from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from details.models import Student,Marks,Attendance
import json
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
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

    #Intent Detection
    intent, score = detect_intent(user_message)

    #Response Generation
    if score == 0:
        reply = (
            "I'm not sure I understood.\n"
            "You can ask about performance, risk level, improvement, study plan or motivation."
        )
    elif score == 1:
        reply = (
            f"I think you're asking about {intent.replace('_', ' ')}.\n"
            "Let me analyze that for you.\n\n"
        )
        reply += generate_response(
            intent,
            average,
            highest_subject,
            lowest_subject,
            trend_direction,
            trend_percentage,
            risk_level,
            subject_trends
        )
    else:
        reply = generate_response(
            intent,
            average,
            highest_subject,
            lowest_subject,
            trend_direction,
            trend_percentage,
            risk_level,
            subject_trends
        )

    return JsonResponse({"reply": reply})

def detect_intent(message):

    stemmer = PorterStemmer()
    message = message.lower()

    # Phrase-Based Direct Mapping (High Priority)
    phrase_map = {
        "how am i doing": "performance_analysis",
        "am i improving": "performance_analysis",
        "how is my performance": "performance_analysis",
        "what about my marks": "performance_analysis",
        "what is my risk": "risk_level",
        "risk level": "risk_level",
        "am i at risk": "risk_level",
        "how can i improve": "improvement_tips",
    }

    for phrase, intent in phrase_map.items():
        if phrase in message:
            return intent, 3 

    #Preprocess
    stop_words = set(stopwords.words("english"))
    words = word_tokenize(message)

    filtered_words = []

    for word in words:
        if word.isalpha() and word not in stop_words:
            stemmed_word = stemmer.stem(word)
            filtered_words.append(stemmed_word)

    #Intent Dictionary
    intent_keywords = {
        "performance_analysis": [
            "analyz", "perform", "progress",
            "result", "mark", "score", "academ", "trend"
        ],
        "study_plan": [
            "studi", "plan", "schedul",
            "prepar", "routin"
        ],
        "improvement_tips": [
            "improv", "better", "increas", "tip"
        ],
        "weak_subject": [
            "weak", "low", "struggl",
            "difficult"
        ],
        "strong_subject": [
            "strong", "best", "highest"
        ],
        "motivation": [
            "sad", "demotiv", "tire", "stress"
        ],
        "risk_level": [
            "risk", "danger", "fail", "drop"
        ]
    }

    # Scoring System
    intent_scores = defaultdict(int)

    for word in filtered_words:
        for intent, keywords in intent_keywords.items():
            if word in keywords:
                intent_scores[intent] += 1

    if intent_scores:
        best_intent = max(intent_scores, key=intent_scores.get)
        best_score = intent_scores[best_intent]
        return best_intent, best_score

    return "unknown", 0

def generate_response(intent, average, highest, lowest,
                      trend_direction, trend_percentage,
                      risk_level, subject_trends):

    # Performance Category
    if average < 60:
        performance = "poor"
    elif average < 80:
        performance = "average"
    else:
        performance = "good"

    # Tone Based On Risk
    if risk_level == "High":
        tone_intro = "Your academic situation needs immediate attention.\n"
    elif risk_level == "Moderate":
        tone_intro = "Your performance is stable but requires improvement.\n"
    else:
        tone_intro = "You are performing well overall.\n"

    #Detect Most Improved & Most Declined Subject
    best_improvement = None
    worst_decline = None

    if subject_trends:
        sorted_trends = sorted(subject_trends, key=lambda x: x["difference"])

        worst_decline = sorted_trends[0]
        best_improvement = sorted_trends[-1]

    
    # PERFORMANCE ANALYSIS
    
    if intent == "performance_analysis":

        response = tone_intro
        response += (
            f"\nYour current average is {average}%.\n"
            f"Compared to the previous exam, you {trend_direction.lower()} "
            f"by {abs(trend_percentage)}%.\n\n"
        )

        # Strong warning if heavy decline
        if trend_percentage <= -10:
            response += (
                "There is a significant drop in your overall performance. "
                "Immediate corrective action is recommended.\n\n"
            )

        # Subject trends
        if subject_trends:
            response += "Subject-level insights:\n"

            for trend in subject_trends:
                response += (
                    f"- {trend['subject']}: {trend['status']} "
                    f"({trend['difference']} marks)\n"
                )

            response += "\n"

            if best_improvement and best_improvement["difference"] > 0:
                response += (
                    f"Great improvement seen in {best_improvement['subject']}.\n"
                )

            if worst_decline and worst_decline["difference"] < 0:
                response += (
                    f"Performance dropped in {worst_decline['subject']}. "
                    "This subject needs priority focus.\n"
                )

        response += (
            f"\nStrongest subject: {highest.subject.subject_name} "
            f"({highest.total_marks})\n"
            f"Weakest subject: {lowest.subject.subject_name} "
            f"({lowest.total_marks})\n\n"
            f"Current Academic Risk Level: {risk_level}"
        )

        return response

   
    # STUDY PLAN
    
    elif intent == "study_plan":

        if risk_level == "High":
            return (
                "You need a strict recovery plan.\n"
                "Study at least 3 focused hours daily.\n"
                "Prioritize weak subjects and practice previous mistakes.\n"
                "Avoid distractions completely."
            )

        elif risk_level == "Moderate":
            return (
                "Follow a structured 2-hour daily revision schedule.\n"
                "Focus more on weaker subjects.\n"
                "Take weekly self-assessment tests."
            )

        else:
            return (
                "Maintain consistency with 1–2 hours of daily revision.\n"
                "Start advanced problem-solving practice for excellence."
            )

    
    # RISK LEVEL
    
    elif intent == "risk_level":

        if risk_level == "High":
            advice = "Immediate improvement is necessary to avoid academic failure."
        elif risk_level == "Moderate":
            advice = "You are not in danger, but improvement is needed."
        else:
            advice = "You are in a safe academic zone. Maintain consistency."

        return (
            f"Your current academic risk level is {risk_level}.\n"
            f"Overall trend: {trend_direction} ({trend_percentage}%).\n"
            f"{advice}"
        )

    
    # IMPROVEMENT TIPS
    
    elif intent == "improvement_tips":

        return (
            f"Your weakest subject is {lowest.subject.subject_name}.\n"
            "Allocate additional daily practice time to this subject.\n"
            "Revise concepts, solve practice papers, and track mistakes carefully.\n"
            f"Current risk level: {risk_level}."
        )

    
    # STRONG SUBJECT
    
    elif intent == "strong_subject":

        return (
            f"Your strongest subject is {highest.subject.subject_name} "
            f"with {highest.total_marks} marks.\n"
            "Continue maintaining this strong performance."
        )

    
    # WEAK SUBJECT
    
    elif intent == "weak_subject":

        return (
            f"Your weakest subject is {lowest.subject.subject_name} "
            f"with {lowest.total_marks} marks.\n"
            "This subject should be your top priority."
        )

    
    # MOTIVATION
    
    elif intent == "motivation":

        if risk_level == "High":
            return (
                "Challenges are temporary.\n"
                "With disciplined effort, improvement is absolutely possible.\n"
                "Start today and stay consistent."
            )
        else:
            return (
                "You are capable of continuous improvement.\n"
                "Consistency and discipline will take you to the next level."
            )

    
    # DEFAULT
    
    else:
        return (
            "I can analyze your academic performance, assess risk levels, "
            "suggest study plans, and provide improvement guidance."
        )