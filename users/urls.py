from django.urls import path
from .views import login_view, admin_dashboard, faculty_dashboard, student_dashboard,logout_view

urlpatterns = [
    path("", login_view, name="login"),
    path("admin-dashboard/", admin_dashboard, name="admin_dashboard"),
    path("faculty-dashboard/", faculty_dashboard, name="faculty_dashboard"),
    path("student-dashboard/", student_dashboard, name="users_student_dashboard"),
    path("logout/", logout_view, name="logout"),

]
