from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from users.models import CustomUser
from details.models import Student, Class, Section
from datetime import date
from django.http import JsonResponse
import pandas as pd

@login_required
def manage_students(request):

    success_count = 0
    failed_row = []
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
        
        # EXCEL UPLOAD LOGIC

        if 'upload_excel' in request.POST:

            excel_file = request.FILES.get("excel_file")

            if not excel_file:
                messages.error(request,"No file selected")
                return redirect("manage_students")

            df = pd.read_excel(excel_file)
            df.columns = df.columns.str.strip().str.lower()
            
            error_dict = {}

            for index, row in df.iterrows():

                try:
                    class_obj = Class.objects.get(
                        class_name=str(row["class"]).strip()
                    )

                    section_obj = Section.objects.get(
                        section_name=str(row["section"]).strip(),
                        class_obj=class_obj
                    )

                    # Username duplicate
                    if CustomUser.objects.filter(
                        username=str(row["username"]).strip()
                    ).exists():
                        raise Exception("Username already exists")

                    # Roll number duplicate
                    if Student.objects.filter(
                        roll_no=str(row["roll_no"]).strip(),
                        class_obj=class_obj,
                        section=section_obj
                    ).exists():
                        raise Exception("Duplicate roll number")

                    user = CustomUser.objects.create(
                        username=str(row["username"]).strip(),
                        password=make_password(str(row["password"])),
                        role="student",
                        is_active=True
                    )

                    joining_date = pd.to_datetime(
                        row["joining_date"],
                        dayfirst=True,
                        errors='coerce'
                    )

                    if pd.isna(joining_date):
                        raise Exception("Invalid joining date")
                    
                    joining_date = joining_date.date()
                    
                    Student.objects.create(
                        user=user,
                        roll_no=str(row["roll_no"]).strip(),
                        name=str(row["name"]).strip(),
                        class_obj=class_obj,
                        section=section_obj,
                        joining_date=joining_date
                    )

                    success_count += 1

                except Exception as e:
                    error_msg = str(e)

                    if error_msg not in error_dict:
                        error_dict[error_msg] = []

                    error_dict[error_msg].append(index + 2)

            if success_count >0:
                messages.success(
                    request,
                    f"{success_count} student uploaded successfully"
                )    

            if error_dict:
                final_errors = []

                for error, rows in error_dict.items():
                    row_list = ", ".join(map(str, rows))
                    final_errors.append(f"Row {row_list}: {error}")

                messages.error(
                    request, "Some rows could not be uploaded:" +":".join(final_errors)
                )

            return redirect("manage_students")

        # NORMAL ADD STUDENT

        username = request.POST.get("username")
        password = request.POST.get("password")
        roll_no = request.POST.get("roll_no")
        name = request.POST.get("name")
        class_id = request.POST.get("class_obj")
        section_id = request.POST.get("section")
        joining_date = request.POST.get("joining_date")

        try:
            if CustomUser.objects.filter(username=username).exists():
                raise Exception("Username already exists")
            
            if Student.objects.filter(
                roll_no=roll_no,
                class_obj_id=class_id,
                section_id=section_id
            ).exists():
                raise Exception("Duplicate roll number")
            

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

            messages.success(request, "Student added successfully")

        except Exception as e:
            messages.error(request, str(e))

        return redirect("manage_students")

    context = {
        "students": students,
        "classes": classes,
        "sections": sections,
        "success_count": success_count,
        "errors":failed_row
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
