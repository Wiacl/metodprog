from django import forms
from .models import Teacher, TeacherInfo, Course, Student


class TeacherForm(forms.ModelForm):
    """Форма для добавления преподавателя"""
    
    class Meta:
        model = Teacher
        fields = ['first_name', 'last_name', 'patronymic', 'email', 'phone', 'hire_date', 'is_active']
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'patronymic': 'Отчество',
            'email': 'Email',
            'phone': 'Телефон',
            'hire_date': 'Дата найма',
            'is_active': 'Активен',
        }
        help_texts = {
            'first_name': 'Введите имя преподавателя',
            'last_name': 'Введите фамилию преподавателя',
            'patronymic': 'Введите отчество преподавателя (необязательно)',
            'email': 'Введите корпоративный email',
            'phone': 'Введите номер телефона (необязательно)',
            'hire_date': 'Выберите дату начала работы',
            'is_active': 'Отметьте, если преподаватель активен',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={
                'placeholder': 'Например: Алексей',
                'class': 'form-control'
            }),
            'last_name': forms.TextInput(attrs={
                'placeholder': 'Например: Иванов',
                'class': 'form-control'
            }),
            'patronymic': forms.TextInput(attrs={
                'placeholder': 'Например: Петрович',
                'class': 'form-control'
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'ivanov@university.ru',
                'class': 'form-control'
            }),
            'phone': forms.TextInput(attrs={
                'placeholder': '+7 (999) 123-45-67',
                'class': 'form-control'
            }),
            'hire_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
                'placeholder': 'ГГГГ-ММ-ДД'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Делаем patronymic и phone необязательными
        self.fields['patronymic'].required = False
        self.fields['phone'].required = False
        self.fields['is_active'].required = False


# Остальные формы остаются без изменений
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