# schedule/views.py
from django.shortcuts import render, redirect
from .forms import TeacherForm
from .data_manager import DataManager
from catalog.data import courses, authors

def teacher_list(request):
    """Страница со списком всех преподавателей"""
    teachers = DataManager.get_all_teachers()
    
    # Для каждого преподавателя получаем его курсы
    for teacher in teachers:
        teacher['courses'] = DataManager.get_courses_for_teacher(teacher['id'])
        # Добавляем email и phone, если их нет в данных
        if 'email' not in teacher:
            teacher['email'] = f"{teacher['name'].lower().replace(' ', '.')}@example.com"
        if 'phone' not in teacher:
            teacher['phone'] = ''
    
    context = {
        'teachers': teachers,
    }
    return render(request, 'schedule/teacher_list.html', context)


def course_list(request):
    """Страница со списком всех курсов"""
    courses_list = DataManager.get_all_courses()
    
    # Для каждого курса получаем его преподавателей
    for course in courses_list:
        course['teachers'] = DataManager.get_teachers_for_course(course['id'])
    
    context = {
        'courses': courses_list,
    }
    return render(request, 'schedule/course_list.html', context)


def add_teacher(request):
    """Страница добавления преподавателя"""
    if request.method == 'POST':
        form = TeacherForm(request.POST)
        
        if form.is_valid():
            # Получаем данные из формы
            teacher_data = {
                'full_name': form.cleaned_data['full_name'],
                'bio': form.cleaned_data.get('bio', ''),
                'specialization': form.cleaned_data.get('specialization', '')
            }
            
            # Добавляем преподавателя
            new_teacher = DataManager.add_teacher(teacher_data)
            
            # Добавляем выбранные курсы к преподавателю
            selected_courses = form.cleaned_data.get('courses', [])
            if selected_courses:
                for course_id in selected_courses:
                    course_id_int = int(course_id)
                    # Находим курс и добавляем ID преподавателя в author_id
                    for course in courses:
                        if course['id'] == course_id_int:
                            if new_teacher['id'] not in course['author_id']:
                                course['author_id'].append(new_teacher['id'])
            
            return redirect('schedule:teacher_list')
        else:
            context = {
                'form': form,
                'error': 'Пожалуйста, исправьте ошибки в форме'
            }
            return render(request, 'schedule/add_teacher.html', context)
    else:
        form = TeacherForm()
        context = {
            'form': form,
        }
        return render(request, 'schedule/add_teacher.html', context)


def add_course(request):
    """Страница добавления курса"""
    return render(request, 'schedule/add_course.html')