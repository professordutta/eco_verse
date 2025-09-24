from django.urls import path
from . import views

app_name = 'learning'

urlpatterns = [
    path('lessons/', views.lesson_list, name='lesson_list'),
    path('lessons/create/', views.lesson_create, name='lesson_create'),
    path('lessons/<slug:slug>/build-quiz/', views.lesson_quiz_build, name='lesson_quiz_build'),
    path('lessons/<slug:slug>/', views.lesson_detail, name='lesson_detail'),
    path('quiz/<int:quiz_id>/', views.quiz_take, name='quiz_take'),
    path('tasks/', views.task_list, name='task_list'),
    path('progress/', views.progress_dashboard, name='progress'),
]