from django.urls import path
from . import views

# Пространство имен для приложения
app_name = 'schedule'

urlpatterns = [
    # Список преподавателей
    path('teachers/', views.teacher_list, name='teacher_list'),
    
    # Список курсов
    path('courses/', views.course_list, name='course_list'),
    
    # Добавление преподавателя
    path('add-teacher/', views.add_teacher, name='add_teacher'),
    
    # Добавление курса
    path('add-course/', views.add_course, name='add_course'),
]