from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from details.models import Student,Marks,Attendance
import json
from collections import defaultdict
from datetime import datetime
from django.http import JsonResponse

def calculate_grade(percentage):
    if percentage >= 90:
        return "A+"
    elif percentage >= 80:
        return "A"
    elif percentage >= 70:
        return "B+"
    elif percentage >= 60:
        return "B"
    elif percentage >= 50:
        return "C"
    else:
        return "D"

@login_required
def dashboard(request):
    student = Student.objects.get(user=request.user)

    # Fetch all marks of this student
    marks = Marks.objects.filter(student=student)

    # Calculate average
    total_score = sum(mark.total_marks for mark in marks)
    total_subjects = marks.count()

    if total_subjects > 0:
        average_score = round(total_score / total_subjects, 2)
    else:
        average_score = 0

    # Attendance calculation
    attendance_records = Attendance.objects.filter(student=student)
    total_days = attendance_records.count()
    present_days = attendance_records.filter(status='P').count()

    if total_days > 0:
        attendance_percentage = round((present_days / total_days) * 100, 2)
    else:
        attendance_percentage = 0

    # Monthly Attendance Trend
    monthly_data = defaultdict(list)

    for record in attendance_records:
        month_key = record.date.strftime("%b %Y")  # Example: "Feb 2026"
        monthly_data[month_key].append(record.status)

    months = []
    monthly_percentages = []

    for month, statuses in monthly_data.items():
        total = len(statuses)
        present = statuses.count('P')

        percentage = round((present / total) * 100, 2)
        months.append(month)
        monthly_percentages.append(percentage)
    

    # Subject-wise data for bar chart
    subject_names = []
    subject_scores = []

    for mark in marks:
        subject_names.append(mark.subject.subject_name)
        subject_scores.append(mark.total_marks)


    context = {
        'student': student,
        'average_score': average_score,
        'attendance_percentage': attendance_percentage,
        'subject_names': json.dumps(subject_names),
        'subject_scores': json.dumps(subject_scores),
        'months': json.dumps(months),
        'monthly_percentages': json.dumps(monthly_percentages)
     }

    return render(request, 'student/dashboard.html', context,)

@login_required
def detailed_marks(request):
    student = Student.objects.get(user=request.user)

    marks = Marks.objects.filter(student=student)

    subject_data = []

    total_internal = 0
    total_external = 0
    total_marks = 0

    for mark in marks:
        percentage = mark.total_marks 
        grade = calculate_grade(percentage)

        subject_data.append({
            "subject": mark.subject.subject_name,
            "internal": mark.internal_marks,
            "external": mark.external_marks,
            "total": mark.total_marks,
            "grade": grade
        })

        total_internal += mark.internal_marks
        total_external += mark.external_marks
        total_marks += mark.total_marks

    subject_count = marks.count()

    if subject_count > 0:
        overall_percentage = round(total_marks / subject_count, 2)
    else:
        overall_percentage = 0

    overall_grade = calculate_grade(overall_percentage)

    context = {
        "student": student,
        "subjects": subject_data,
        "total_internal": total_internal,
        "total_external": total_external,
        "total_marks": total_marks,
        "overall_percentage": overall_percentage,
        "overall_grade": overall_grade
    }

    return render(request, "student/detailed_marks.html", context)

@login_required
def ai_feedback(request):
    student = Student.objects.get(user=request.user)
    marks = Marks.objects.filter(student=student)

    strong_subject = None
    weak_subject = None
    average = 0
    prediction = ""
    study_plan_text = ""

    if marks.exists():

        total_score = 0
        subject_count = 0

        for mark in marks:
            total_score += mark.total_marks
            subject_count += 1

            if not strong_subject or mark.total_marks > strong_subject.total_marks:
                strong_subject = mark

            if not weak_subject or mark.total_marks < weak_subject.total_marks:
                weak_subject = mark

        average = round(total_score / subject_count, 2)

        # Study plan logic based on performance
        if average < 60:
            study_plan_text = "Recommended 3 hrs/day. Focus strongly on weak subjects."
            prediction = "Expected improvement: 15-20% with consistent effort."

        elif average < 80:
            study_plan_text = "Recommended 2 hrs/day for weak subjects, 1 hr for strong ones."
            prediction = "Expected improvement: 8-10% with consistent effort."

        else:
            study_plan_text = "Maintain 1–2 hrs/day revision. Focus on advanced preparation."
            prediction = "You can reach 90%+ with disciplined consistency."

    context = {
        "student": student,
        "strong_subject": strong_subject,
        "weak_subject": weak_subject,
        "average": average,
        "study_plan_text": study_plan_text,
        "prediction": prediction
    }

    return render(request, "student/ai_feedback.html", context)

@login_required
@csrf_exempt
def ai_response(request):
    if request.method == "POST":
        data = json.loads(request.body)
        action = data.get("action")

        student = Student.objects.get(user=request.user)

        # ---------------- LEVEL 1: ANALYZE PERFORMANCE ----------------
        if action == "analyze":

            marks = Marks.objects.filter(student=student)

            if not marks.exists():
                return JsonResponse({
                    "message": "No marks data available to analyze."
                })

            total_score = 0
            subject_count = 0

            highest_subject = None
            lowest_subject = None

            for mark in marks:
                total_score += mark.total_marks
                subject_count += 1

                if not highest_subject or mark.total_marks > highest_subject.total_marks:
                    highest_subject = mark

                if not lowest_subject or mark.total_marks < lowest_subject.total_marks:
                    lowest_subject = mark

            average = round(total_score / subject_count, 2)

            # Performance classification
            if average < 60:
                performance = "poor"
            elif average < 80:
                performance = "average"
            else:
                performance = "good"

            request.session["performance"] = performance

            # Dynamic Message
            if performance == "poor":
                message = (
                    f"I analyzed your marks 📊\n\n"
                    f"Your overall average is {average}%.\n\n"
                    f"Your strongest subject: {highest_subject.subject.subject_name} "
                    f"({highest_subject.total_marks})\n"
                    f"Your weakest subject: {lowest_subject.subject.subject_name} "
                    f"({lowest_subject.total_marks})\n\n"
                    "Don't worry — improvement is completely possible 💪"
                )

            elif performance == "average":
                message = (
                    f"Good effort 👍\n\n"
                    f"Your overall average is {average}%.\n\n"
                    f"Strongest subject: {highest_subject.subject.subject_name} "
                    f"({highest_subject.total_marks})\n"
                    f"Needs more focus: {lowest_subject.subject.subject_name} "
                    f"({lowest_subject.total_marks})\n\n"
                    "You're close to excellence!"
                )

            else:
                message = (
                    f"Excellent performance 🎉\n\n"
                    f"Your overall average is {average}%.\n\n"
                    f"Best subject: {highest_subject.subject.subject_name} "
                    f"({highest_subject.total_marks})\n"
                    f"Keep an eye on: {lowest_subject.subject.subject_name} "
                    f"({lowest_subject.total_marks})\n\n"
                    "Maintain this consistency!"
                )

            return JsonResponse({
                "message": message,
                "next_level": "actions"
            })

        # ---------------- LEVEL 2: ACTIONS ----------------
        performance = request.session.get("performance")

        if not performance:
            return JsonResponse({
                "message": "Please analyze your performance first."
            })

        if action == "study_plan":

            if performance == "poor":
                message = (
                    "📘 Study Plan:\n\n"
                    "• Study 2–3 hours daily\n"
                    "• Focus first on weak subject\n"
                    "• Practice previous year questions\n"
                    "• Weekly self-assessment"
                )

            elif performance == "average":
                message = (
                    "📘 Study Plan:\n\n"
                    "• Revise 1.5–2 hours daily\n"
                    "• Strengthen weak topics\n"
                    "• Take mock tests every weekend\n"
                    "• Improve speed & accuracy"
                )

            else:
                message = (
                    "📘 Study Plan:\n\n"
                    "• Maintain daily revision\n"
                    "• Solve advanced problems\n"
                    "• Mentor peers\n"
                    "• Focus on competitive-level preparation"
                )

        elif action == "analysis":

            message = (
                "📊 Subject Analysis:\n\n"
                "Detailed marks breakdown is available in the "
                "Detailed Marks page.\n"
                "Review internal and external performance separately."
            )

        elif action == "tips":

            message = (
                "💡 Improvement Tips:\n\n"
                "• Stay consistent\n"
                "• Avoid last-minute studying\n"
                "• Revise weekly\n"
                "• Practice writing answers clearly"
            )

        else:
            return JsonResponse({"message": "Invalid request"})

        message += "\n\nKeep working hard and stay focused 🚀"

        return JsonResponse({
            "message": message,
            "next_level": "end"
        })

    return JsonResponse({"message": "Invalid request"}, status=400)