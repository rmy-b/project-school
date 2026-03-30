from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from details.models import Student,Marks,Attendance
import json
import requests
from collections import defaultdict
from datetime import datetime
from django.http import JsonResponse
import os
from dotenv import load_dotenv

load_dotenv()

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

    # Get latest exam for this student
    latest_exam = Marks.objects.filter(student=student)\
        .order_by('-exam__id')\
        .values_list('exam', flat=True)\
        .first()

    # Fetch marks only for latest exam
    marks = Marks.objects.filter(student=student, exam=latest_exam)

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

    # Order attendance by date (important)
    attendance_records = Attendance.objects.filter(student=student).order_by('date')

    monthly_data = defaultdict(list)

    for record in attendance_records:
        month_key = record.date.strftime("%b %Y")
        monthly_data[month_key].append(record.status)

    # Convert month strings back to datetime for proper sorting
    sorted_months = sorted(
        monthly_data.keys(),
        key=lambda x: datetime.strptime(x, "%b %Y")
    )

    # Keep only last 4 months
    sorted_months = sorted_months[-4:]

    months = []
    monthly_percentages = []

    for month in sorted_months:
        statuses = monthly_data[month]
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

    # Get latest exam for this student
    latest_exam = Marks.objects.filter(student=student)\
        .order_by('-exam__id')\
        .values_list('exam', flat=True)\
        .first()

    # Fetch marks only for latest exam
    marks = Marks.objects.filter(student=student, exam=latest_exam)

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

     # Get all exams for this student ordered latest first
    exam_ids = Marks.objects.filter(student=student)\
        .order_by('-exam__id')\
        .values_list('exam', flat=True)\
        .distinct()

    latest_exam = exam_ids[0] if len(exam_ids) > 0 else None
    previous_exam = exam_ids[1] if len(exam_ids) > 1 else None

    marks = Marks.objects.filter(student=student, exam=latest_exam)
    previous_marks = Marks.objects.filter(student=student, exam=previous_exam) if previous_exam else None

    strong_subject = None
    weak_subject = None
    average = 0
    prediction = ""
    trend_percentage = 0
    trend_direction = "No previous data"
    risk_level = "Low"

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


        if previous_marks and previous_marks.exists():

            prev_total = sum(m.total_marks for m in previous_marks)
            prev_count = previous_marks.count()
            prev_average = round(prev_total / prev_count, 2)

            trend_percentage = round(average - prev_average, 2)

            if trend_percentage > 0:
                trend_direction = "Improved"
            elif trend_percentage < 0:
                trend_direction = "Declined"
            else:
                trend_direction = "No Change"

        risk_points = 0

        # Low average
        if average < 50:
            risk_points += 2

        # Attendance risk
        attendance_records = Attendance.objects.filter(student=student)
        total_days = attendance_records.count()
        present_days = attendance_records.filter(status='P').count()

        attendance_percentage = (present_days / total_days * 100) if total_days > 0 else 0

        if attendance_percentage < 75:
            risk_points += 1

        # Negative trend
        if trend_percentage < 0:
            risk_points += 1

        # Final Risk Level
        if risk_points == 0:
            risk_level = "Low"
        elif risk_points <= 2:
            risk_level = "Moderate"
        else:
            risk_level = "High"

        if previous_marks and previous_marks.exists():

            projected_next = average + trend_percentage

            if trend_percentage > 0:
                prediction = f"If this trend continues, you may score around {round(projected_next,2)}% in the next exam."
            elif trend_percentage < 0:
                prediction = "Your performance is declining. Immediate corrective action is recommended."
            else:
                prediction = "Your performance is stable. With extra effort, you can improve further."
        else:
            prediction = "Insufficient historical data for performance prediction."

    context = {
        "student": student,
        "strong_subject": strong_subject,
        "weak_subject": weak_subject,
        "average": average,
        "prediction": prediction,
        "trend_direction": trend_direction,
        "trend_percentage": trend_percentage,
        "risk_level": risk_level
    }

    return render(request, "student/ai_feedback.html", context)


def get_ai_reply(user_message, student_data):

    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
    "Authorization": f"Bearer {os.getenv('GROQ_API_KEY')}",
    "Content-Type": "application/json"
    }

    system_prompt = """
    You are an AI Study Assistant.

    Rules:
    - Only answer academic and study-related questions.
    - If the question is unrelated, politely say you can help with studies.

    Response Behaviour(VERY IMPORTANT):
    - If the user greets(hi, hello, hey) -> respond briefly and naturally like a human.
    - If the user asks a simple question -> give a short answer(1-3 lines).
    - If the user asks for tips -> give short bullet points.
    - If the user asks for analysis -> give structured detailed response with headings.
    - Do NOT over-explain unnecessarily.
    - Keep responses clean, readable, and appropriate to the question.

    Style:
    - Use headings only when needed
    - Use bullet points for tips
    - Be friendly and natural
    """

    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": student_data + "\n\n" + user_message}
        ]
    }

    response = requests.post(url, headers=headers, json=payload)

    data = response.json()

    print("FULL RESPONSE:", data)

    if "choices" in data:
        return data["choices"][0]["message"]["content"]
    else:
        return "AI error:" + str(data)

@login_required
def ai_response(request):

    if request.method != "POST":
        return JsonResponse({"reply": "Invalid request"}, status=400)

    data = json.loads(request.body)
    user_message = data.get("message", "").lower()

    student = Student.objects.get(user=request.user)

    # Get Exams
    exam_ids = Marks.objects.filter(student=student)\
        .order_by('-exam__id')\
        .values_list('exam', flat=True)\
        .distinct()

    latest_exam = exam_ids[0] if len(exam_ids) > 0 else None
    previous_exam = exam_ids[1] if len(exam_ids) > 1 else None

    marks = Marks.objects.filter(student=student, exam=latest_exam)
    previous_marks = Marks.objects.filter(student=student, exam=previous_exam) if previous_exam else None

    if not marks.exists():
        return JsonResponse({"reply": "No marks data available."})

    #Current Exam Analytics
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

    #Trend Calculation
    trend_percentage = 0
    trend_direction = "No previous data"

    if previous_marks and previous_marks.exists():
        prev_total = sum(m.total_marks for m in previous_marks)
        prev_count = previous_marks.count()
        prev_average = round(prev_total / prev_count, 2)

        trend_percentage = round(average - prev_average, 2)

        if trend_percentage > 0:
            trend_direction = "Improved"
        elif trend_percentage < 0:
            trend_direction = "Declined"
        else:
            trend_direction = "No Change"

    #Subject-wise Trend
    subject_trends = []

    if previous_marks and previous_marks.exists():

        current_dict = {m.subject.subject_name: m.total_marks for m in marks}
        previous_dict = {m.subject.subject_name: m.total_marks for m in previous_marks}

        for subject, current_mark in current_dict.items():

            previous_mark = previous_dict.get(subject)

            if previous_mark is not None:
                difference = current_mark - previous_mark

                if difference > 5:
                    status = "Improved"
                elif difference < -5:
                    status = "Declined"
                else:
                    status = "Stable"

                subject_trends.append({
                    "subject": subject,
                    "difference": difference,
                    "status": status
                })

    #Risk Engine
    risk_points = 0

    if average < 50:
        risk_points += 2

    low_subjects = marks.filter(total_marks__lt=40).count()
    if low_subjects > 2:
        risk_points += 1

    attendance_records = Attendance.objects.filter(student=student)
    total_days = attendance_records.count()
    present_days = attendance_records.filter(status='P').count()
    attendance_percentage = (present_days / total_days * 100) if total_days > 0 else 0

    if attendance_percentage < 75:
        risk_points += 1

    if trend_percentage < 0:
        risk_points += 1

    if risk_points == 0:
        risk_level = "Low"
    elif risk_points <= 2:
        risk_level = "Moderate"
    else:
        risk_level = "High"

    # Prepare student data (PERSONALIZED AI ) 
    student_data = f"""
    Student Academic Data:
    Average Score: {average}%
    Strong Subject: {highest_subject.subject.subject_name}
    Weak Subject: {lowest_subject.subject.subject_name}
    Trend: {trend_direction} ({trend_percentage}%)
    Risk Level: {risk_level}
    """

    # Call AI
    reply = get_ai_reply(user_message, student_data)

    return JsonResponse({"reply": reply})
