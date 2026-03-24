from django.shortcuts import render, redirect
from django.contrib import messages
from details.models import Faculty
from users.models import CustomUser
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import pandas as pd

@login_required
def manage_faculty(request):

    if request.method == "POST":

        if "bulk_upload" in request.POST:
            handle_bulk_upload(request)
            return redirect('manage_faculty')   

        name = request.POST.get("name")
        qualification = request.POST.get("qualification")
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Check if username already exists
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "This user already exists.")
            return redirect("manage_faculty")

        # Create user
        user = CustomUser.objects.create(
            username=username,
            role="faculty"
        )

        # Hash password
        user.set_password(password)
        user.save()

        # Create faculty record
        Faculty.objects.create(
            user=user,
            name=name,
            qualification=qualification
        )

        messages.success(request, "Faculty added successfully.")

        return redirect("manage_faculty")

    faculty_list = Faculty.objects.select_related("user").all()

    context = {
        "faculty_list": faculty_list
    }

    return render(request, "adminpanel/manage_faculty.html", context)

def handle_bulk_upload(request):

    file = request.FILES.get("file")

    if not file:
        messages.error(request, "No file uploaded")
        return

    try:
        import pandas as pd

        if file.name.endswith('.csv'):
            df = pd.read_csv(file)
        else:
            df = pd.read_excel(file)

        success_count = 0

        for index, row in df.iterrows():

            username = str(row.get('username', '')).strip()
            if username == '' or username.lower() == 'nan':
                continue

            # Avoid duplicate users
            if CustomUser.objects.filter(username=username).exists():
                continue

            # Create user
            user = CustomUser.objects.create_user(
                username=username,
                password=str(row['password']),
                role='faculty'
            )

            # Create faculty
            Faculty.objects.create(
                user=user,
                name=row['name'],
                qualification=row['qualification']
            )

            success_count += 1

        messages.success(request, f"{success_count} Faculties uploaded successfully")

    except Exception as e:
        messages.error(request, f"Error: {str(e)}")

#UPDATE FACULTY
@login_required
def update_faculty(request):

    if request.method == "POST":

        faculty_id = request.POST.get("faculty_id")

        name = request.POST.get("name")
        qualification = request.POST.get("qualification")
        username = request.POST.get("username")

        new_password = request.POST.get("new_password")

        faculty = Faculty.objects.get(id=faculty_id)
        user = faculty.user

        # update faculty fields
        faculty.name = name
        faculty.qualification = qualification

        # check username change
        if user.username != username:
            if CustomUser.objects.filter(username=username).exists():
                messages.error(request, "This user already exists.")
                return redirect("manage_faculty")

            user.username = username

        # reset password (only if entered)
        if new_password:
            user.set_password(new_password)

        faculty.save()
        user.save()

        messages.success(request, "Faculty updated successfully.")

    return redirect("manage_faculty")

# DELETE FACULTY
@login_required
def delete_faculty(request):

    if request.method == "POST":

        faculty_id = request.POST.get("faculty_id")

        faculty = Faculty.objects.get(id=faculty_id)

        # delete both faculty and user
        faculty.user.delete()

        messages.success(request, "Faculty deleted successfully.")

    return redirect("manage_faculty")



# TOGGLE-STATUS
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
@login_required
def toggle_faculty_status(request):

    if request.method == "POST":

        data = json.loads(request.body)

        faculty_id = data.get("faculty_id")
        status = data.get("status")

        faculty = Faculty.objects.get(id=faculty_id)

        faculty.user.is_active = status
        faculty.user.save()

        return JsonResponse({"success": True})

    return JsonResponse({"success": False})