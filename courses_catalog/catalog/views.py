from django.shortcuts import render
from django.http import Http404
from . import data

def index(request):
    """Главная страница"""
    return render(request, 'index.html')

def courses_list(request):
    """Список всех курсов"""
    context = {
        'courses': data.courses
    }
    return render(request, 'courses.html', context)

def course_detail(request, course_id):
    """Детальная страница курса"""
    # Ищем курс по id
    course = next((c for c in data.courses if c['id'] == course_id), None)
    
    if course:
        # Находим ВСЕХ авторов курса по их ID из списка author_ids
        course_authors = [a for a in data.authors if a['id'] in course['author_id']]
        
        context = {
            'course': course,
            'authors': course_authors  # Передаем список авторов
        }
        return render(request, 'course_detail.html', context)
    else:
        return render(request, 'not_found.html', status=404)

def authors_list(request):
    """Список всех авторов"""
    context = {
        'authors': data.authors
    }
    return render(request, 'authors.html', context)

def author_detail(request, author_id):
    """Детальная страница автора"""
    # Ищем автора по id
    author = next((a for a in data.authors if a['id'] == author_id), None)
    
    if author:
        
        author_courses = [c for c in data.courses if author_id in c['author_id']]
        
        context = {
            'author': author,
            'courses': author_courses
        }
        return render(request, 'author_details.html', context)
    else:
        return render(request, 'not_found.html', status=404)

def info(request):
    """Страница информации"""
    return render(request, 'info.html')

def custom_404(request, exception=None):
    """Кастомная страница 404"""
    return render(request, 'not_found.html', status=404)