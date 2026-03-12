from django.urls import path

from .views.dashboard_views import admin_dashboard
from .views.managestudent_views import manage_students,get_sections,edit_student,delete_student,toggle_student_status



urlpatterns = [
    path("dashboard/", admin_dashboard, name="admin_dashboard"),
    path("students/", manage_students, name="manage_students"),
    path("get-sections/", get_sections, name="get_sections"),
    path("edit-student/",edit_student, name="edit_student"),
    path("delete-student/",delete_student,name="delete_student"),
    path("toggle-student-status/",toggle_student_status,name="toggle_student_status"),




    
]