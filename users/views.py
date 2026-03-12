from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from users.models import CustomUser
def login_view(request):

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        role = request.POST.get("role")

        user = authenticate(request, username=username, password=password)

        # If authenticate fails, check if user exists but inactive
        if user is None:

            try:
                existing_user = CustomUser.objects.get(username=username)

                if not existing_user.is_active:
                    messages.error(request, "Account is inactive")
                    return redirect("login")

            except CustomUser.DoesNotExist:
                pass

            messages.error(request, "Invalid credentials")
            return redirect("login")

        # Role check
        if user.role != role:
            messages.error(request, "Role mismatch!")
            return redirect("login")
        
        # if user is not None:

        #     if user.role != role:
        #         messages.error(request, "Role mismatch!")
        #         return redirect("login")

        #     if not user.is_active:
        #         messages.error(request, "Account is inactive")
        #         return redirect("login")

        login(request, user)

        if role == "admin":
            return redirect("admin_dashboard")
        elif role == "faculty":
            return redirect("faculty_dashboard")
        elif role == "student":
            return redirect("student_dashboard")

        # else:
        #     messages.error(request, "Invalid credentials")

    return render(request, "users/login.html")


@login_required
def admin_dashboard(request):
    if request.user.role != "admin":
        return redirect("login")
    return HttpResponse('<h2>Welcome Admin</h2><a href="/logout/">Logout</a>')


@login_required
def faculty_dashboard(request):
    if request.user.role != "faculty":
        return redirect("login")
    return HttpResponse('<h2>Welcome Faculty</h2><a href="/logout/">Logout</a>')


@login_required
def student_dashboard(request):
    if request.user.role != "student":
        return redirect("login")
    return HttpResponse('<h2>Welcome Student</h2><a href="/logout/">Logout</a>')

def logout_view(request):
    logout(request)
    return redirect("login")
