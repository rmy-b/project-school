from django.shortcuts import render
from details.models import Class, Section, Subject, Student, Marks, Exam,Attendance
from django.db.models import Avg
from .ml_model import train_model, predict_pass_rate
import json

def reports_analytics(request):

    selected_class = request.GET.get("class")
    selected_section = request.GET.get("section")
    selected_exam = request.GET.get("exam")

    # Default Class = 6
    if not selected_class:
        selected_class = Class.objects.filter(class_name="6").first()
    else:
        selected_class = Class.objects.get(id=selected_class)

    # Default Section = A
    if not selected_section:
        selected_section = Section.objects.filter(
            section_name="A",
            class_obj=selected_class
        ).first()
    else:
        selected_section = Section.objects.get(id=selected_section)

    # Default Exam
    if not selected_exam:
        selected_exam = Exam.objects.first()
    else:
        selected_exam = Exam.objects.get(id=selected_exam)

    students = Student.objects.filter(
        class_obj=selected_class,
        section=selected_section
    )

    subjects = Subject.objects.filter(class_obj=selected_class)

    total_students = students.count()

    passed_students = 0

    subject_pass_data = []
    subject_risk_data = []

    risk_table = []
    unique_risk_students = set()   # for unique count

    # -----------------------------
    # SUBJECT-WISE CALCULATION
    # -----------------------------
    for subject in subjects:

        marks = Marks.objects.filter(
            student__in=students,
            subject=subject,
            exam=selected_exam
        )

        total = marks.count()

        # PASS: >= 35
        pass_count = marks.filter(total_marks__gte=35).count()

        # FAIL (real risk): < 35
        fail_count = marks.filter(total_marks__lt=35).count()

        pass_rate = (pass_count / total * 100) if total > 0 else 0

        subject_pass_data.append({
            "subject": subject.subject_name,
            "pass_rate": round(pass_rate, 2)
        })

        subject_risk_data.append({
            "subject": subject.subject_name,
            "risk": fail_count
        })

        # -----------------------------
        # RISK TABLE (ONLY FAILING STUDENTS)
        # -----------------------------
        risk_marks = marks.filter(total_marks__lt=35)

        for m in risk_marks:
            risk_table.append({
                "roll": m.student.roll_no,
                "name": m.student.name,
                "subject": subject.subject_name,
                "marks": m.total_marks
            })

            # Track unique students
            unique_risk_students.add(m.student.id)

    # -----------------------------
    # OVERALL PASS RATE (CORRECT LOGIC)
    # -----------------------------
    for student in students:

        student_marks = Marks.objects.filter(
            student=student,
            exam=selected_exam
        )

        # If ANY subject < 35 → FAIL
        failed = student_marks.filter(total_marks__lt=35).exists()

        if not failed:
            passed_students += 1

    overall_pass_rate = (
        (passed_students / total_students) * 100
        if total_students > 0 else 0
    )

               
    # ML PREDICTION
    # -----------------------------------
    predicted_pass_rate = 0
    ml_data = []

    for student in students:

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

        # ATTENDANCE
        attendance_qs = Attendance.objects.filter(student=student)

        total_days = attendance_qs.count()
        present_days = attendance_qs.filter(status='P').count()

        attendance_percentage = (present_days / total_days * 100) if total_days > 0 else 0

        # LABEL
        label = 1 if mid_avg >= 35 else 0

        ml_data.append({
            "unit_avg": unit_avg,
            "mid_avg": mid_avg,
            "attendance": attendance_percentage,
            "label": label
        })

    # TRAIN MODEL
    model = train_model(ml_data)

    # PREPARE INPUT
    predict_input = []

    for item in ml_data:
        predict_input.append([
            item['unit_avg'],
            item['mid_avg'],
            item['attendance']
        ])

      # TRAIN MODEL ONLY IF DATA EXISTS
    if len(ml_data) > 0:

        model = train_model(ml_data)

        predict_input = [
            [item['unit_avg'], item['mid_avg'], item['attendance']]
            for item in ml_data
        ]

        if model is None:
            predicted_pass_rate = overall_pass_rate
        else:
            predicted_pass_rate = predict_pass_rate(model, predict_input)

    else:
        predicted_pass_rate = 0
    # -----------------------------
    # CONTEXT
    # -----------------------------
    context = {

        "classes": Class.objects.all(),
        "sections": Section.objects.filter(class_obj=selected_class),
        "exams": Exam.objects.all(),

        "selected_class": selected_class,
        "selected_section": selected_section,
        "selected_exam": selected_exam,

        "overall_pass_rate": round(overall_pass_rate, 2),

        # UNIQUE RISK COUNT
        "risk_count": len(unique_risk_students),

        "pass_chart": json.dumps(subject_pass_data),
        "risk_chart": json.dumps(subject_risk_data),

        "risk_students": risk_table,
        "predicted_pass_rate": predicted_pass_rate,
    }

    return render(request, "adminpanel/reports.html", context)