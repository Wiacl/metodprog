from django import forms
from django.core.exceptions import ValidationError
from .models import Teacher, TeacherInfo, Course, Student
import re
from datetime import date


# ========== ВАЛИДАТОРЫ ==========

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
    class Meta:
        model = Teacher
        fields = '__all__'
        widgets = {
            'hire_date': forms.DateInput(attrs={
                'type': 'date', 
                'class': 'form-control',
                'placeholder': 'ГГГГ-ММ-ДД'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите имя (например: Алексей)'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите фамилию (например: Иванов)'
            }),
            'patronymic': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите отчество (например: Петрович)'
            }),
            'position': forms.Select(attrs={
                'class': 'form-select',
                'placeholder': 'Выберите должность'
            }),
            'employee_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'EMP-123456'
            }),
            'salary': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '30000 - 500000'
            }),
            'work_experience_years': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0-60 лет'
            }),
            'rating': forms.NumberInput(attrs={
                'class': 'form-control', 
                'step': '0.01',
                'placeholder': '0.00 - 5.00'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'teacher@university.ru'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+7 (999) 123-45-67'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
    
    def clean_phone(self):
        """АВТОМАТИЧЕСКОЕ ФОРМАТИРОВАНИЕ телефона"""
        phone = self.cleaned_data.get('phone')
        if not phone:
            return phone
        
        digits = re.sub(r'[^\d+]', '', phone)
        
        if digits.startswith('8'):
            digits = '+7' + digits[1:]
        elif digits.startswith('9') and len(digits) == 10:
            digits = '+7' + digits
        
        if not re.match(r'^\+7\d{10}$', digits):
            raise ValidationError('Неверный формат номера. Введите 10 цифр после +7 или 8')
        
        formatted = f'+7 ({digits[2:5]}) {digits[5:8]}-{digits[8:10]}-{digits[10:12]}'
        return formatted
    
    def clean_employee_id(self):
        """АВТОМАТИЧЕСКОЕ ФОРМАТИРОВАНИЕ табельного номера"""
        employee_id = self.cleaned_data.get('employee_id')
        if not employee_id:
            return employee_id
        
        cleaned = re.sub(r'[^A-Za-z0-9]', '', employee_id.upper())
        
        if cleaned.startswith('EMP'):
            num_part = cleaned[3:]
        else:
            num_part = cleaned
        
        digits = re.sub(r'[^\d]', '', num_part)[-6:]
        
        if len(digits) != 6:
            raise ValidationError('Табельный номер должен содержать 6 цифр')
        
        return f'EMP-{digits}'
    
    def clean_email(self):
        """АВТОМАТИЧЕСКОЕ ПРИВЕДЕНИЕ email к нижнему регистру"""
        email = self.cleaned_data.get('email')
        if email:
            return email.lower().strip()
        return email
    
    def clean_first_name(self):
        """АВТОМАТИЧЕСКОЕ ФОРМАТИРОВАНИЕ имени"""
        name = self.cleaned_data.get('first_name')
        if name:
            return name.strip().capitalize()
        return name
    
    def clean_last_name(self):
        """АВТОМАТИЧЕСКОЕ ФОРМАТИРОВАНИЕ фамилии"""
        name = self.cleaned_data.get('last_name')
        if name:
            return name.strip().capitalize()
        return name
    
    def clean(self):
        """Общая валидация формы"""
        cleaned_data = super().clean()
        
        position = cleaned_data.get('position')
        salary = cleaned_data.get('salary')
        rating = cleaned_data.get('rating')
        experience = cleaned_data.get('work_experience_years')
        
        if position == 'professor' and salary and salary < 100000:
            self.add_error('salary', 'Профессор не может получать меньше 100 000 руб')
        
        if rating and experience:
            if rating > 4.5 and experience < 5:
                self.add_error('rating', 'Высокий рейтинг требует минимум 5 лет стажа')
        
        return cleaned_data


# ========== ФОРМА ИНФОРМАЦИИ О ПРЕПОДАВАТЕЛЕ ==========

class TeacherInfoForm(forms.ModelForm):
    class Meta:
        model = TeacherInfo
        fields = '__all__'
        exclude = ['teacher']
        widgets = {
            'bio': forms.Textarea(attrs={
                'rows': 4, 
                'class': 'form-control',
                'placeholder': 'Расскажите о преподавателе: образование, достижения, научные интересы...'
            }),
            'degree': forms.Select(attrs={
                'class': 'form-select',
                'placeholder': 'Выберите ученую степень'
            }),
            'specialization': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Например: Математический анализ, Базы данных, Программирование'
            }),
            'office_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Например: 301, 405, А-208'
            }),
            'years_of_experience': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0-50 лет'
            }),
            'publications_count': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Количество научных публикаций'
            }),
            'scientific_degree_year': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'ГГГГ (например: 2010)'
            }),
            'consulting_hours': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Например: Пн 14:00-16:00, Ср 10:00-12:00'
            }),
        }
    
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
        fields = '__all__'
        widgets = {
            'start_date': forms.DateInput(attrs={
                'type': 'date', 
                'class': 'form-control',
                'placeholder': 'ГГГГ-ММ-ДД'
            }),
            'end_date': forms.DateInput(attrs={
                'type': 'date', 
                'class': 'form-control',
                'placeholder': 'ГГГГ-ММ-ДД'
            }),
            'description': forms.Textarea(attrs={
                'rows': 4, 
                'class': 'form-control',
                'placeholder': 'Подробное описание курса: чему научатся студенты, какие темы будут изучены...'
            }),
            'prerequisites': forms.Textarea(attrs={
                'rows': 3, 
                'class': 'form-control',
                'placeholder': 'Что должен знать студент: например, "базовые знания Python", "опыт работы с базами данных"...'
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите название курса (например: "Программирование на Python")'
            }),
            'level': forms.Select(attrs={
                'class': 'form-select',
                'placeholder': 'Выберите уровень сложности'
            }),
            'credits': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '1-12 кредитов'
            }),
            'max_students': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '1-100 студентов'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Стоимость курса в рублях'
            }),
            'duration_weeks': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '1-52 недели'
            }),
            'certificate_available': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
    
    def clean_title(self):
        """АВТОМАТИЧЕСКОЕ ФОРМАТИРОВАНИЕ названия курса"""
        title = self.cleaned_data.get('title')
        if title:
            return ' '.join(word.capitalize() for word in title.strip().split())
        return title
    
    def clean_price(self):
        """АВТОМАТИЧЕСКОЕ ОКРУГЛЕНИЕ цены"""
        price = self.cleaned_data.get('price')
        if price:
            return round(price, 2)
        return price
    
    def clean(self):
        """Общая валидация"""
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        
        if start_date and end_date and start_date > end_date:
            self.add_error('start_date', 'Дата начала не может быть позже даты окончания')
        
        return cleaned_data


# ========== ФОРМА СТУДЕНТА ==========

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'
        widgets = {
            'date_of_birth': forms.DateInput(attrs={
                'type': 'date', 
                'class': 'form-control',
                'placeholder': 'ГГГГ-ММ-ДД'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите имя (например: Иван)'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите фамилию (например: Петров)'
            }),
            'patronymic': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите отчество (например: Иванович)'
            }),
            'student_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'ST-123456'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'student@university.ru'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+7 (999) 123-45-67'
            }),
            'parent_phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+7 (999) 123-45-67'
            }),
            'address': forms.Textarea(attrs={
                'rows': 3, 
                'class': 'form-control',
                'placeholder': 'Город, улица, дом, квартира'
            }),
            'average_grade': forms.NumberInput(attrs={
                'class': 'form-control', 
                'step': '0.01',
                'placeholder': '0.00 - 5.00'
            }),
            'scholarship_amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Сумма стипендии в рублях'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
    
    def clean_phone(self):
        """АВТОМАТИЧЕСКОЕ ФОРМАТИРОВАНИЕ телефона студента"""
        phone = self.cleaned_data.get('phone')
        if not phone:
            return phone
        
        digits = re.sub(r'[^\d+]', '', phone)
        
        if digits.startswith('8'):
            digits = '+7' + digits[1:]
        elif digits.startswith('9') and len(digits) == 10:
            digits = '+7' + digits
        
        if not re.match(r'^\+7\d{10}$', digits):
            raise ValidationError('Неверный формат номера')
        
        return f'+7 ({digits[2:5]}) {digits[5:8]}-{digits[8:10]}-{digits[10:12]}'
    
    def clean_student_id(self):
        """АВТОМАТИЧЕСКОЕ ФОРМАТИРОВАНИЕ номера студенческого"""
        student_id = self.cleaned_data.get('student_id')
        if not student_id:
            return student_id
        
        cleaned = re.sub(r'[^A-Za-z0-9]', '', student_id.upper())
        
        if cleaned.startswith('ST'):
            num_part = cleaned[2:]
        else:
            num_part = cleaned
        
        digits = re.sub(r'[^\d]', '', num_part)[-6:]
        
        if len(digits) != 6:
            raise ValidationError('Номер студенческого должен содержать 6 цифр')
        
        return f'ST-{digits}'
    
    def clean_email(self):
        """АВТОМАТИЧЕСКОЕ ПРИВЕДЕНИЕ email к нижнему регистру"""
        email = self.cleaned_data.get('email')
        if email:
            return email.lower().strip()
        return email
    
    def clean_date_of_birth(self):
        """Проверка возраста"""
        dob = self.cleaned_data.get('date_of_birth')
        if dob:
            age = date.today().year - dob.year
            if age < 16:
                raise ValidationError('Студент должен быть старше 16 лет')
            if age > 100:
                raise ValidationError('Некорректная дата рождения')
        return dob
    
    def clean(self):
        """Общая валидация"""
        cleaned_data = super().clean()
        average_grade = cleaned_data.get('average_grade')
        scholarship = cleaned_data.get('scholarship_amount')
        
        if average_grade and scholarship:
            if average_grade < 3.0 and scholarship > 0:
                self.add_error('scholarship_amount', 'Студенты с успеваемостью ниже 3.0 не получают стипендию')
        
        return cleaned_data