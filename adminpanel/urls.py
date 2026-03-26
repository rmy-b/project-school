from django.urls import path
from .views.reports_views import reports_analytics
from .views.managefaculty_views import manage_faculty,toggle_faculty_status,update_faculty,delete_faculty
from .views.dashboard_views import admin_dashboard
from .views.managestudent_views import manage_students,get_sections,edit_student,delete_student,toggle_student_status

from .views.manageclass_views import manage_classes,class_section_detail,export_classes_excel

urlpatterns = [
    path("dashboard/", admin_dashboard, name="admin_dashboard"),
    path("students/", manage_students, name="manage_students"),
    path("get-sections/", get_sections, name="get_sections"),
    path("edit-student/",edit_student, name="edit_student"),
    path("delete-student/",delete_student,name="delete_student"),
    path("toggle-student-status/",toggle_student_status,name="toggle_student_status"),
    path("classes/", manage_classes, name="manage_classes"),
    path("class/<int:class_id>/section/<int:section_id>/",class_section_detail,name="class_section_detail"),
    path("export-excel", export_classes_excel, name="export_classes_excel"),


    


















path("manage_faculty/", manage_faculty,name="manage_faculty"),
path("faculty-active-status/", toggle_faculty_status, name="toggle_faculty_status"),
path("update-faculty/" , update_faculty,name="update_faculty"),
path("delete-faculty/" , delete_faculty,name="delete_faculty"),
path("reports/" ,reports_analytics,name="reports_analytics"),

]
