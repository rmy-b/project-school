from django.shortcuts import render
from details.models import Class, Section, Student, Faculty, Marks, Exam,Attendance
import json
from django.db.models import Avg
from .ml_model import train_model, predict_pass_rate
from django.contrib.auth.decorators import login_required

@login_required
def admin_dashboard(request):

    classes = Class.objects.all()
    exam = Exam.objects.first()

    # -----------------------------
    # TOP CARDS DATA
    # -----------------------------
    total_students = Student.objects.count()
    total_faculty = Faculty.objects.count()
    total_classes = Section.objects.count()   # as you requested

    overall_students = 0
    overall_passed = 0
    overall_risk = 0

    pass_chart = []
    risk_chart = []

    # -----------------------------
    # CLASS-WISE CALCULATION
    # -----------------------------
    for cls in classes:

        students = Student.objects.filter(class_obj=cls)
        total = students.count()

        passed = 0
        risk = 0

        for student in students:

            marks = Marks.objects.filter(student=student, exam=exam)

            if not marks.exists():
                continue

            failed = marks.filter(total_marks__lt=35).exists()

            if failed:
                risk += 1
                overall_risk += 1
            else:
                passed += 1
                overall_passed += 1

        overall_students += total

        pass_rate = (passed / total * 100) if total > 0 else 0

        pass_chart.append({
            "class": f"Class {cls.class_name}",
            "rate": round(pass_rate, 2)
        })

        risk_chart.append({
            "class": f"Class {cls.class_name}",
            "risk": risk
        })

    overall_pass_rate = (
        (overall_passed / overall_students) * 100
        if overall_students > 0 else 0
    )
    # -----------------------------------
    # AI PREDICTED OVERALL PASS %
    # -----------------------------------
    predicted_school_pass = 0
    ml_data = []

    all_students = Student.objects.all()

    for student in all_students:

    # UNIT AVG
        unit_avg = Marks.objects.filter(
            student=student,
            exam__exam_name__icontains="Unit"
            ).aggregate(avg=Avg('total_marks'))['avg'] or 0

    # MID AVG
        mid_avg = Marks.objects.filter(
            student=student,
            exam__exam_name__icontains="Mid"
            ).aggregate(avg=Avg('total_marks'))['avg'] or 0

        # ATTENDANCE %
        attendance_qs = Attendance.objects.filter(student=student)

        total_days = attendance_qs.count()
        present_days = attendance_qs.filter(status='P').count()

        attendance_percentage = (
                (present_days / total_days) * 100
            if total_days > 0 else 0
            )

         # LABEL
        label = 1 if mid_avg >= 35 else 0

        ml_data.append({
            "unit_avg": unit_avg,
            "mid_avg": mid_avg,
            "attendance": attendance_percentage,
            "label": label
        })

        # TRAIN + PREDICT
        if len(ml_data) > 0:

            model = train_model(ml_data)

            predict_input = [
            [item['unit_avg'], item['mid_avg'], item['attendance']]
            for item in ml_data
            ]

            if model is None:
                predicted_school_pass = overall_pass_rate
            else:
                predicted_school_pass = predict_pass_rate(model, predict_input)

    context = {
        "total_students": total_students,
        "total_faculty": total_faculty,
        "total_classes": total_classes,
        "overall_risk": overall_risk,

        "overall_pass_rate": round(overall_pass_rate, 2),
        "predicted_school_pass": predicted_school_pass,
        "pass_chart": json.dumps(pass_chart),
        "risk_chart": json.dumps(risk_chart),
    }

    return render(request, "adminpanel/dashboard.html", context)