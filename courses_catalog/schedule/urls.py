from django.urls import path
from . import views

app_name = 'schedule'

urlpatterns = [
    # Teacher URLs
    path('teachers/', views.TeacherListView.as_view(), name='teacher_list'),
    path('teachers/<int:pk>/', views.TeacherDetailView.as_view(), name='teacher_detail'),
    path('teachers/create/', views.TeacherCreateView.as_view(), name='teacher_create'),
    path('teachers/<int:pk>/update/', views.TeacherUpdateView.as_view(), name='teacher_update'),
    path('teachers/<int:pk>/delete/', views.TeacherDeleteView.as_view(), name='teacher_delete'),
    
    # Course URLs
    path('courses/', views.CourseListView.as_view(), name='course_list'),
    path('courses/create/', views.CourseCreateView.as_view(), name='course_create'),
    path('courses/<int:pk>/update/', views.CourseUpdateView.as_view(), name='course_update'),
    path('courses/<int:pk>/delete/', views.CourseDeleteView.as_view(), name='course_delete'),
    
    # Student URLs
    path('students/', views.StudentListView.as_view(), name='student_list'),
    path('students/<int:pk>/', views.StudentDetailView.as_view(), name='student_detail'),  # ЭТОТ МАРШРУТ БЫЛ ОТСУТСТВУЕТ
    path('students/<int:pk>/update/', views.StudentUpdateView.as_view(), name='student_update'),
    path('students/<int:pk>/delete/', views.StudentDeleteView.as_view(), name='student_delete'),
    path('students/<int:pk>/enroll/', views.StudentEnrollView.as_view(), name='student_enroll'),
    path('students/<int:pk>/unenroll/', views.StudentUnenrollView.as_view(), name='student_unenroll'),
    
    # ORM Queries
    path('orm-queries/', views.ORMQueriesView.as_view(), name='orm_queries'),
]