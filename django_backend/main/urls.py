from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('life-wheel/', views.life_wheel, name='life_wheel'),
    path('assessments/', views.assessments, name='assessments'),
    path('ai-coach/', views.ai_coach, name='ai_coach'),
    path('profile/', views.profile, name='profile'),
    path('register/', views.register_view, name='register'),
    path('ai-report/<int:report_id>/', views.ai_report_view, name='ai_report'),
]
