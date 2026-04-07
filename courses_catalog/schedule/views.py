from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Count
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Teacher, TeacherInfo, Course, Student
from .forms import TeacherForm, TeacherInfoForm, CourseForm, StudentForm


# Teacher Views
class TeacherListView(ListView):
    model = Teacher
    template_name = 'schedule/teacher_list.html'
    context_object_name = 'teachers'
    paginate_by = 10


class TeacherDetailView(DetailView):
    model = Teacher
    template_name = 'schedule/teacher_detail.html'
    context_object_name = 'teacher'


class TeacherCreateView(CreateView):
    model = Teacher
    form_class = TeacherForm
    template_name = 'schedule/teacher_form.html'
    success_url = reverse_lazy('schedule:teacher_list')

    def form_valid(self, form):
        messages.success(self.request, 'Преподаватель успешно создан')
        return super().form_valid(form)


class TeacherUpdateView(UpdateView):
    model = Teacher
    form_class = TeacherForm
    template_name = 'schedule/teacher_form.html'
    success_url = reverse_lazy('schedule:teacher_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if hasattr(self.object, 'info') and self.object.info:
            context['info_form'] = TeacherInfoForm(instance=self.object.info)
        else:
            context['info_form'] = TeacherInfoForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        teacher_form = self.get_form()
        
        if hasattr(self.object, 'info') and self.object.info:
            info_form = TeacherInfoForm(request.POST, instance=self.object.info)
        else:
            info_form = TeacherInfoForm(request.POST)
        
        if teacher_form.is_valid() and info_form.is_valid():
            teacher = teacher_form.save()
            info = info_form.save(commit=False)
            info.teacher = teacher
            info.save()
            messages.success(request, 'Данные преподавателя обновлены')
            return redirect('schedule:teacher_detail', pk=teacher.pk)
        
        return self.render_to_response(self.get_context_data(
            form=teacher_form,
            info_form=info_form
        ))


class TeacherDeleteView(DeleteView):
    model = Teacher
    template_name = 'schedule/teacher_confirm_delete.html'
    success_url = reverse_lazy('schedule:teacher_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Преподаватель успешно удален')
        return super().delete(request, *args, **kwargs)


# Course Views
class CourseListView(ListView):
    model = Course
    template_name = 'schedule/course_list.html'
    context_object_name = 'courses'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        teacher_id = self.request.GET.get('teacher')
        if teacher_id:
            queryset = queryset.filter(teacher_id=teacher_id)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['teachers'] = Teacher.objects.all()
        context['selected_teacher'] = self.request.GET.get('teacher', '')
        return context


class CourseCreateView(CreateView):
    model = Course
    form_class = CourseForm
    template_name = 'schedule/course_form.html'
    success_url = reverse_lazy('schedule:course_list')

    def form_valid(self, form):
        messages.success(self.request, 'Курс успешно создан')
        return super().form_valid(form)


class CourseUpdateView(UpdateView):
    model = Course
    form_class = CourseForm
    template_name = 'schedule/course_form.html'
    success_url = reverse_lazy('schedule:course_list')

    def form_valid(self, form):
        messages.success(self.request, 'Курс успешно обновлен')
        return super().form_valid(form)


class CourseDeleteView(DeleteView):
    model = Course
    template_name = 'schedule/course_confirm_delete.html'
    success_url = reverse_lazy('schedule:course_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Курс успешно удален')
        return super().delete(request, *args, **kwargs)


# Student Views добавить Create
class StudentListView(ListView):
    model = Student
    template_name = 'schedule/student_list.html'
    context_object_name = 'students'
    paginate_by = 10


class StudentDetailView(DetailView):
    model = Student
    template_name = 'schedule/student_detail.html'
    context_object_name = 'student'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['available_courses'] = Course.objects.exclude(id__in=self.object.courses.all())
        return context

class StudentCreateView(CreateView):  
    """Создание нового студента"""
    model = Student
    form_class = StudentForm
    template_name = 'schedule/student_form.html'
    success_url = reverse_lazy('schedule:student_list')

    def form_valid(self, form):
        messages.success(self.request, 'Студент успешно создан')
        return super().form_valid(form)

class StudentUpdateView(UpdateView):
    model = Student
    form_class = StudentForm
    template_name = 'schedule/student_form.html'
    success_url = reverse_lazy('schedule:student_list')

    def form_valid(self, form):
        messages.success(self.request, 'Данные студента обновлены')
        return super().form_valid(form)


class StudentDeleteView(DeleteView):
    model = Student
    template_name = 'schedule/student_confirm_delete.html'
    success_url = reverse_lazy('schedule:student_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Студент успешно удален')
        return super().delete(request, *args, **kwargs)


# Student Course Management
class StudentEnrollView(View):
    def post(self, request, pk):
        student = get_object_or_404(Student, pk=pk)
        course_id = request.POST.get('course_id')
        course = get_object_or_404(Course, pk=course_id)
        
        if course.students.count() < course.max_students:
            student.courses.add(course)
            messages.success(request, f'Студент {student} записан на курс {course}')
        else:
            messages.error(request, f'Курс {course} переполнен')
        
        return redirect('schedule:student_detail', pk=pk)


class StudentUnenrollView(View):
    def post(self, request, pk):
        student = get_object_or_404(Student, pk=pk)
        course_id = request.POST.get('course_id')
        course = get_object_or_404(Course, pk=course_id)
        
        student.courses.remove(course)
        messages.success(request, f'Студент {student} отписан от курса {course}')
        
        return redirect('schedule:student_detail', pk=pk)


# ORM Query Views
class ORMQueriesView(View):
    def get(self, request):
        # Все студенты курса (пример для первого курса)
        course = Course.objects.first()
        course_students = course.students.all() if course else []
        
        # Все преподаватели, у которых больше 2 курсов
        teachers_with_many_courses = Teacher.objects.annotate(
            course_count=Count('courses')
        ).filter(course_count__gt=2)
        
        # Студенты без курсов
        students_without_courses = Student.objects.filter(courses__isnull=True)
        
        # Преподаватели без профиля
        teachers_without_profile = Teacher.objects.filter(info__isnull=True)
        
        # Статистика
        teachers_count = Teacher.objects.count()
        courses_count = Course.objects.count()
        students_count = Student.objects.count()
        
        context = {
            'course': course,
            'course_students': course_students,
            'teachers_with_many_courses': teachers_with_many_courses,
            'students_without_courses': students_without_courses,
            'teachers_without_profile': teachers_without_profile,
            'teachers_count': teachers_count,
            'courses_count': courses_count,
            'students_count': students_count,
        }
        
        return render(request, 'schedule/orm_queries.html', context)