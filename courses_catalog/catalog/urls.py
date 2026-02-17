from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('courses/', views.courses_list, name='courses'),
    path('course/<int:course_id>/', views.course_detail, name='course_detail'),
    path('authors/', views.authors_list, name='authors'),
    path('author/<int:author_id>/', views.author_detail, name='author_detail'),
    path('info/', views.info, name='info'),
]