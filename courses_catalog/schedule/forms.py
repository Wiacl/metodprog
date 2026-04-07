from django import forms
from .models import Teacher, TeacherInfo, Course, Student


class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['first_name', 'last_name', 'patronymic', 'email', 'phone', 'hire_date', 'is_active']
        widgets = {
            'hire_date': forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'patronymic': 'Отчество',
            'email': 'Email',
            'phone': 'Телефон',
            'hire_date': 'Дата найма',
            'is_active': 'Активен',
        }


class TeacherInfoForm(forms.ModelForm):
    class Meta:
        model = TeacherInfo
        fields = ['degree', 'specialization', 'bio', 'office_number', 'years_of_experience']
        labels = {
            'degree': 'Ученая степень',
            'specialization': 'Специализация',
            'bio': 'Биография',
            'office_number': 'Номер кабинета',
            'years_of_experience': 'Лет опыта',
        }


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description', 'teacher', 'level', 'credits', 
                  'max_students', 'start_date', 'end_date', 'is_active']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'title': 'Название курса',
            'description': 'Описание',
            'teacher': 'Преподаватель',
            'level': 'Уровень',
            'credits': 'Кредиты',
            'max_students': 'Максимум студентов',
            'start_date': 'Дата начала',
            'end_date': 'Дата окончания',
            'is_active': 'Активен',
        }


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'patronymic', 'email', 'phone', 
                  'date_of_birth', 'address', 'is_active']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'patronymic': 'Отчество',
            'email': 'Email',
            'phone': 'Телефон',
            'date_of_birth': 'Дата рождения',
            'address': 'Адрес',
            'is_active': 'Активен',
        }