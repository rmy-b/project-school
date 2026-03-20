from django.urls import path
from .views.reports_views import reports_analytics
from .views.managefaculty_views import manage_faculty,toggle_faculty_status,update_faculty,delete_faculty
from .views.dashboard_views import admin_dashboard

urlpatterns = [
    path("dashboard/", admin_dashboard, name="admin_dashboard"),














path("manage_faculty/", manage_faculty,name="manage_faculty"),
path("faculty-active-status/", toggle_faculty_status, name="toggle_faculty_status"),
path("update-faculty/" , update_faculty,name="update_faculty"),
path("delete-faculty/" , delete_faculty,name="delete_faculty"),
path("reports/" ,reports_analytics,name="reports_analytics"),

]
