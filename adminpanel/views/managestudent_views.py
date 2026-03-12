from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from users.models import CustomUser
from details.models import Student, Class, Section
from datetime import date
from django.http import JsonResponse

@login_required
def manage_students(request):

    classes = Class.objects.all()
    sections = Section.objects.all()

    students = Student.objects.select_related(
        "user", "class_obj", "section"
    )

    # ---------- FILTER LOGIC ----------
    class_id = request.GET.get("class")
    section_id = request.GET.get("section")

    if class_id:
        students = students.filter(class_obj_id=class_id)

    if section_id:
        students = students.filter(section_id=section_id)

    # ---------- ADD STUDENT ----------
    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")
        roll_no = request.POST.get("roll_no")
        name = request.POST.get("name")
        class_id = request.POST.get("class_obj")
        section_id = request.POST.get("section")
        joining_date = request.POST.get("joining_date")

        user = CustomUser.objects.create(
            username=username,
            password=make_password(password),
            role="student",
            is_active=True
        )

        Student.objects.create(
            user=user,
            roll_no=roll_no,
            name=name,
            class_obj_id=class_id,
            section_id=section_id,
            joining_date=joining_date
        )

        return redirect("manage_students")

    context = {
        "students": students,
        "classes": classes,
        "sections": sections
    }

    return render(request, "adminpanel/manage_students.html", context)

def get_sections(request):

    class_id = request.GET.get("class_id")

    sections = Section.objects.filter(class_obj_id=class_id)

    data = []

    for section in sections:
        data.append({
            "id": section.id,
            "name": section.section_name
        })

    return JsonResponse(data, safe=False)


@login_required
def edit_student(request):

    if request.method == "POST":

        student_id = request.POST.get("student_id")
        name = request.POST.get("name")
        username = request.POST.get("username")
        new_password = request.POST.get("new_password")

        student = Student.objects.select_related("user").get(id=student_id)

        # update student name
        student.name = name
        student.save()

        # update username
        student.user.username = username

        # reset password if provided
        if new_password:
            student.user.password = make_password(new_password)

        student.user.save()

    return redirect("manage_students")


@login_required
def delete_student(request):

    if request.method == "POST":

        student_id = request.POST.get("student_id")

        student = Student.objects.get(id=student_id)

        student.delete()

    return redirect("manage_students")

@login_required
def toggle_student_status(request):

    if request.method == "POST":

        student_id = request.POST.get("student_id")

        student = Student.objects.select_related("user").get(id=student_id)

        student.user.is_active = not student.user.is_active
        student.user.save()

        return JsonResponse({"status": "success"})
