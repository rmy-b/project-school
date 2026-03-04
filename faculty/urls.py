from django.urls import path
from . import views

urlpatterns = [
    path('', views.faculty_dashboard, name='faculty_dashboard'),
    path('marks/',views.marks_page, name='marks_page'),
    path('attendance/', views.attendance_page, name="attendance_page"),
    path('performance/',views.performance_view, name="performance_view"),
    path('attendance/report/',views.generate_attendance_report, name="attendance_report"),

]
