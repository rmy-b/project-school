from django.shortcuts import render
from details.models import Class, Section, Student, Faculty, Marks, Exam
import json


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

    context = {
        "total_students": total_students,
        "total_faculty": total_faculty,
        "total_classes": total_classes,
        "overall_risk": overall_risk,

        "overall_pass_rate": round(overall_pass_rate, 2),

        "pass_chart": json.dumps(pass_chart),
        "risk_chart": json.dumps(risk_chart),
    }

    return render(request, "adminpanel/dashboard.html", context)