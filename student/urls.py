from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='student_dashboard'),
    path('detailed-marks/', views.detailed_marks, name='detailed_marks'),
    path('ai-feedback/', views.ai_feedback, name='ai_feedback'),
    path('ai-response/', views.ai_response, name='ai_response'),
]
