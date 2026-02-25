from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from details.models import Faculty, FacultyAssignment,Student, Marks, Exam, Attendance
import datetime


@login_required
def faculty_dashboard(request):
    user = request.user   # CustomUser

    # Get Faculty linked to this user
    faculty = Faculty.objects.get(user=user)

    # Get all assignments of this faculty
    assignments = FacultyAssignment.objects.filter(faculty=faculty)

    # Incharge class (if any)
    incharge = assignments.filter(is_class_incharge=True).first()

    # Classes handled (unique)
    classes_handled = assignments.values(
        'class_obj__class_name',
        'section__section_name',
        'subject__subject_name'
    ).distinct()

    context = {
        "faculty": faculty,
        "incharge": incharge,
        "classes_handled": classes_handled,
    }

    return render(request, "faculty/dashboard.html", context)

#Marks Page
# @login_required
# def marks_page(request):
#     user = request.user
#     faculty = Faculty.objects.get(user=user)

#     # Subjects & classes this faculty teaches
#     assignments = FacultyAssignment.objects.filter(faculty=faculty)

#     context = {
#         "faculty": faculty,
#         "assignments": assignments,
#     }

#     return render(request, "faculty/marks.html", context)
@login_required
def marks_page(request):
    faculty = Faculty.objects.get(user=request.user)

    # All classes this teacher handles
    assignments = FacultyAssignment.objects.filter(faculty=faculty)
    exams = Exam.objects.all()

    selected_class_id = request.GET.get('class')
    selected_exam_id = request.GET.get('exam')

    students = []
    marks_data = []

    # Default class = class incharge class
    default_assignment = assignments.filter(is_class_incharge=True).first()

    if not selected_class_id and default_assignment:
        selected_class_id = str(default_assignment.class_obj.id)

    selected_assignment = None

    if selected_class_id:
        selected_assignment = assignments.filter(class_obj_id=selected_class_id).first()

    # ---------------- SAVE MARKS (POST) ----------------
    if request.method == "POST":
        selected_class_id = request.POST.get("class")
        selected_exam_id = request.POST.get("exam")

        selected_assignment = assignments.filter(class_obj_id=selected_class_id).first()
        exam = Exam.objects.filter(id=selected_exam_id).first()

        # Safety check (prevents crash)
        if not exam or not selected_assignment:
            return redirect(f"/faculty/marks/?class={selected_class_id}&exam={selected_exam_id}")

        students = Student.objects.filter(
            class_obj=selected_assignment.class_obj,
            section=selected_assignment.section
        )

        for student in students:
            internal = request.POST.get(f"internal_{student.id}")
            external = request.POST.get(f"external_{student.id}")

            if internal is not None and external is not None:
                internal_val = float(internal or 0)
                external_val = float(external or 0)
                total = internal_val + external_val

                Marks.objects.update_or_create(
                    student=student,
                    subject=selected_assignment.subject,
                    exam=exam,
                    defaults={
                        "internal_marks": internal_val,
                        "external_marks": external_val,
                        "total_marks": total,
                    }
                )

        # Redirect after POST (prevents resubmission)
        return redirect(f"/faculty/marks/?class={selected_class_id}&exam={selected_exam_id}")
    # ---------------------------------------------------

    # ---------------- DISPLAY MARKS (GET) ----------------
    if selected_assignment and selected_exam_id:
        exam = Exam.objects.filter(id=selected_exam_id).first()

        if exam:
            students = Student.objects.filter(
                class_obj=selected_assignment.class_obj,
                section=selected_assignment.section
            )

            for student in students:
                mark = Marks.objects.filter(
                    student=student,
                    subject=selected_assignment.subject,
                    exam=exam
                ).first()

                marks_data.append({
                    'student': student,
                    'internal': mark.internal_marks if mark else '',
                    'external': mark.external_marks if mark else '',
                    'total': mark.total_marks if mark else '',
                })
    # -----------------------------------------------------

    context = {
        'faculty': faculty,
        'assignments': assignments,
        'students': students,
        'marks_data': marks_data,
        'exams': exams,
        'selected_exam_id': selected_exam_id,
        'selected_class_id': selected_class_id,
        'selected_assignment': selected_assignment,
    }

    return render(request, 'faculty/marks.html', context)

@login_required
def attendance_page(request):
    faculty = Faculty.objects.get(user=request.user)

    # Check if this faculty is class incharge
    class_incharge = FacultyAssignment.objects.filter(
        faculty=faculty,
        is_class_incharge=True
    ).first()

    # ❌ Not class teacher
    if not class_incharge:
        return render(request, 'faculty/attendance.html', {
            'not_authorized': True
        })

    # ✅ Class teacher
    class_obj = class_incharge.class_obj
    section = class_incharge.section

    students = Student.objects.filter(
        class_obj=class_obj,
        section=section
    )

    error_message = None

    # Get date
    if request.method == "POST":
        selected_date = request.POST.get("date")

        if not selected_date:
            error_message = "Please select a date"
            selected_date = datetime.date.today()
        else:
            selected_date = datetime.datetime.strptime(selected_date, "%Y-%m-%d").date()
    else:
        selected_date = datetime.date.today()

    # ---------------- SAVE ATTENDANCE ----------------
    if request.method == "POST" and not error_message:
        for student in students:
            checkbox_value = request.POST.get(f"present_{student.id}")

            status = "P" if checkbox_value == "on" else "A"

            Attendance.objects.update_or_create(
                student=student,
                date=selected_date,
                defaults={
                    'status': status
                }
            )
    # ------------------------------------------------

    # Load existing attendance
    attendance_data = []
    present_count = 0
    absent_count = 0

    for student in students:
        record = Attendance.objects.filter(
            student=student,
            date=selected_date
        ).first()

        if record:
            status = record.status
        else:
            status = "P"  # default

        if status == "P":
            present_count += 1
        else:
            absent_count += 1

        attendance_data.append({
            'student': student,
            'status': status
        })

    context = {
        'faculty': faculty,
        'class_obj': class_obj,
        'section': section,
        'students': students,
        'attendance_data': attendance_data,
        'selected_date': selected_date,
        'present_count': present_count,
        'absent_count': absent_count,
        'total_count': students.count(),
        'error_message': error_message,
        'not_authorized': False
    }

    return render(request, 'faculty/attendance.html', context)