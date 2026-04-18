from django import forms
from django.core.exceptions import ValidationError
from .models import Teacher, TeacherInfo, Course, Student
import re
from datetime import date


# ========== КАСТОМНЫЕ ВАЛИДАТОРЫ ==========

def validate_phone_number(value):
    """Кастомный валидатор для номера телефона"""
    if value:
        pattern = r'^\+7 \(\d{3}\) \d{3}-\d{2}-\d{2}$'
        if not re.match(pattern, value):
            raise ValidationError('Телефон должен быть в формате: +7 (999) 123-45-67')


def validate_fio_length(value):
    """Валидатор для проверки длины ФИО"""
    if len(value) < 2:
        raise ValidationError('Поле должно содержать минимум 2 символа')
    if len(value) > 50:
        raise ValidationError('Поле должно содержать максимум 50 символов')


def validate_future_date(value):
    """Валидатор для проверки даты в будущем"""
    if value and value > date.today():
        raise ValidationError('Дата не может быть в будущем')


def validate_positive_number(value):
    """Валидатор для положительных чисел"""
    if value is not None and value < 0:
        raise ValidationError('Значение не может быть отрицательным')


# ========== ФОРМА ПРЕПОДАВАТЕЛЯ ==========

class TeacherForm(forms.ModelForm):
    """Форма на основе модели Teacher"""
    
    class Meta:
        model = Teacher
        fields = [
            'first_name', 'last_name', 'patronymic', 'position',
            'employee_id', 'salary', 'work_experience_years', 'rating',
            'email', 'phone', 'hire_date', 'is_active'
        ]
        widgets = {
            'hire_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите имя'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите фамилию'}),
            'patronymic': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите отчество'}),
            'position': forms.Select(attrs={'class': 'form-select'}),
            'employee_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'EMP-123456'}),
            'salary': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '30000'}),
            'work_experience_years': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
            'rating': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': '5.00'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'teacher@university.ru'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+7 (999) 123-45-67'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'patronymic': 'Отчество',
            'position': 'Должность',
            'employee_id': 'Табельный номер',
            'salary': 'Зарплата (руб)',
            'work_experience_years': 'Стаж работы (лет)',
            'rating': 'Рейтинг (0-5)',
            'email': 'Email',
            'phone': 'Телефон',
            'hire_date': 'Дата найма',
            'is_active': 'Активен',
        }
        help_texts = {
            'employee_id': 'Формат: EMP-123456',
            'salary': 'Минимум 30 000 руб, максимум 500 000 руб',
            'rating': 'Оценка от 0 до 5',
            'phone': 'Формат: +7 (999) 123-45-67',
        }
    
    # ========== МЕТОДЫ clean_ДЛЯ ПОЛЕЙ ==========
    
    def clean_employee_id(self):
        """Проверка формата табельного номера"""
        employee_id = self.cleaned_data.get('employee_id')
        pattern = r'^EMP-\d{6}$'
        if not re.match(pattern, employee_id):
            raise ValidationError('Табельный номер должен быть в формате: EMP-123456')
        return employee_id
    
    def clean_phone(self):
        """Проверка формата телефона"""
        phone = self.cleaned_data.get('phone')
        if phone:
            pattern = r'^\+7 \(\d{3}\) \d{3}-\d{2}-\d{2}$'
            if not re.match(pattern, phone):
                raise ValidationError('Телефон должен быть в формате: +7 (999) 123-45-67')
        return phone
    
    def clean_salary(self):
        """Проверка зарплаты"""
        salary = self.cleaned_data.get('salary')
        if salary < 30000:
            raise ValidationError('Зарплата не может быть меньше 30 000 руб')
        if salary > 500000:
            raise ValidationError('Зарплата не может быть больше 500 000 руб')
        return salary
    
    def clean_work_experience_years(self):
        """Проверка стажа работы"""
        experience = self.cleaned_data.get('work_experience_years')
        if experience > 60:
            raise ValidationError('Стаж не может превышать 60 лет')
        if experience > 0:
            hire_date = self.cleaned_data.get('hire_date')
            if hire_date:
                age_at_hire = date.today().year - hire_date.year
                if experience > age_at_hire:
                    raise ValidationError('Стаж не может быть больше, чем период работы в организации')
        return experience
    
    # ========== МЕТОД clean() ДЛЯ ФОРМЫ ==========
    
    def clean(self):
        """Общая валидация формы"""
        cleaned_data = super().clean()
        
        # Валидация 1: Проверка соответствия должности и зарплаты
        position = cleaned_data.get('position')
        salary = cleaned_data.get('salary')
        
        if position == 'professor' and salary and salary < 100000:
            self.add_error('salary', 'Профессор не может получать меньше 100 000 руб')
        
        if position == 'assistant' and salary and salary > 80000:
            self.add_error('salary', 'Ассистент не может получать больше 80 000 руб')
        
        # Валидация 2: Проверка соответствия рейтинга и стажа
        rating = cleaned_data.get('rating')
        experience = cleaned_data.get('work_experience_years')
        
        if rating and experience:
            if rating > 4.5 and experience < 5:
                self.add_error('rating', 'Высокий рейтинг требует минимум 5 лет стажа')
            if rating < 3.0 and experience > 10:
                self.add_error('rating', 'При таком стаже рейтинг не может быть ниже 3.0')
        
        return cleaned_data


# ========== ФОРМА ИНФОРМАЦИИ О ПРЕПОДАВАТЕЛЕ ==========

class TeacherInfoForm(forms.ModelForm):
    class Meta:
        model = TeacherInfo
        fields = ['degree', 'specialization', 'bio', 'office_number', 
                  'years_of_experience', 'publications_count', 
                  'scientific_degree_year', 'consulting_hours']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'degree': forms.Select(attrs={'class': 'form-select'}),
            'specialization': forms.TextInput(attrs={'class': 'form-control'}),
            'office_number': forms.TextInput(attrs={'class': 'form-control'}),
            'years_of_experience': forms.NumberInput(attrs={'class': 'form-control'}),
            'publications_count': forms.NumberInput(attrs={'class': 'form-control'}),
            'scientific_degree_year': forms.NumberInput(attrs={'class': 'form-control'}),
            'consulting_hours': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    # Методы clean_ для полей
    def clean_publications_count(self):
        count = self.cleaned_data.get('publications_count')
        if count and count > 500:
            raise ValidationError('Количество публикаций не может превышать 500')
        return count
    
    def clean_scientific_degree_year(self):
        year = self.cleaned_data.get('scientific_degree_year')
        if year:
            if year < 1950:
                raise ValidationError('Год не может быть раньше 1950')
            if year > date.today().year:
                raise ValidationError('Год не может быть в будущем')
        return year
    
    # Метод clean() для формы
    def clean(self):
        cleaned_data = super().clean()
        degree = cleaned_data.get('degree')
        degree_year = cleaned_data.get('scientific_degree_year')
        experience = cleaned_data.get('years_of_experience')
        
        if degree and degree in ['docent', 'professor'] and not degree_year:
            self.add_error('scientific_degree_year', 'Для доцента/профессора необходимо указать год получения степени')
        
        if degree and degree == 'professor' and experience and experience < 10:
            self.add_error('years_of_experience', 'Для получения степени профессора требуется минимум 10 лет опыта')
        
        return cleaned_data


# ========== ФОРМА КУРСА ==========

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description', 'teacher', 'level', 'credits',
                  'max_students', 'start_date', 'end_date', 'is_active',
                  'price', 'duration_weeks', 'prerequisites', 'certificate_available']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'prerequisites': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'level': forms.Select(attrs={'class': 'form-select'}),
            'credits': forms.NumberInput(attrs={'class': 'form-control'}),
            'max_students': forms.NumberInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'duration_weeks': forms.NumberInput(attrs={'class': 'form-control'}),
            'certificate_available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    # Методы clean_ для полей
    def clean_credits(self):
        credits = self.cleaned_data.get('credits')
        if credits < 1:
            raise ValidationError('Кредиты не могут быть меньше 1')
        if credits > 12:
            raise ValidationError('Кредиты не могут быть больше 12')
        return credits
    
    def clean_max_students(self):
        max_students = self.cleaned_data.get('max_students')
        if max_students < 1:
            raise ValidationError('Максимум студентов не может быть меньше 1')
        if max_students > 100:
            raise ValidationError('Максимум студентов не может быть больше 100')
        return max_students
    
    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price and price < 0:
            raise ValidationError('Цена не может быть отрицательной')
        return price
    
    # Метод clean() для формы
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        credits = cleaned_data.get('credits')
        duration_weeks = cleaned_data.get('duration_weeks')
        
        # Валидация дат
        if start_date and end_date:
            if start_date > end_date:
                self.add_error('start_date', 'Дата начала не может быть позже даты окончания')
            if start_date < date.today():
                self.add_error('start_date', 'Дата начала не может быть в прошлом')
        
        # Валидация соответствия кредитов и длительности
        if credits and duration_weeks:
            expected_credits = duration_weeks // 3  # Примерно 1 кредит на 3 недели
            if abs(credits - expected_credits) > 2:
                self.add_error('credits', f'Для длительности {duration_weeks} недель ожидается {expected_credits} кредитов')
        
        return cleaned_data


# ========== ФОРМА СТУДЕНТА ==========

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'patronymic', 'student_id',
                  'email', 'phone', 'date_of_birth', 'address',
                  'average_grade', 'parent_phone', 'scholarship_amount', 'is_active']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'patronymic': forms.TextInput(attrs={'class': 'form-control'}),
            'student_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ST-123456'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'average_grade': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'parent_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'scholarship_amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    # Методы clean_ для полей
    def clean_student_id(self):
        student_id = self.cleaned_data.get('student_id')
        pattern = r'^ST-\d{6}$'
        if not re.match(pattern, student_id):
            raise ValidationError('Номер студенческого должен быть в формате: ST-123456')
        return student_id
    
    def clean_average_grade(self):
        grade = self.cleaned_data.get('average_grade')
        if grade and (grade < 0 or grade > 5):
            raise ValidationError('Средний балл должен быть в диапазоне от 0 до 5')
        return grade
    
    def clean_date_of_birth(self):
        dob = self.cleaned_data.get('date_of_birth')
        if dob:
            age = date.today().year - dob.year
            if age < 16:
                raise ValidationError('Студент должен быть старше 16 лет')
            if age > 100:
                raise ValidationError('Некорректная дата рождения')
        return dob
    
    # Метод clean() для формы
    def clean(self):
        cleaned_data = super().clean()
        average_grade = cleaned_data.get('average_grade')
        scholarship = cleaned_data.get('scholarship_amount')
        
        # Стипендия зависит от успеваемости
        if average_grade and scholarship:
            if average_grade < 3.0 and scholarship > 0:
                self.add_error('scholarship_amount', 'Студенты с успеваемостью ниже 3.0 не получают стипендию')
            if average_grade >= 4.5 and scholarship < 2000:
                self.add_error('scholarship_amount', 'Отличники должны получать стипендию не менее 2000 руб')
        
        # Проверка телефонов
        phone = cleaned_data.get('phone')
        parent_phone = cleaned_data.get('parent_phone')
        
        if phone == parent_phone and phone:
            self.add_error('parent_phone', 'Телефон студента и родителей не должны совпадать')
        
        return cleaned_data