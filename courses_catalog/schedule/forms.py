# schedule/forms.py
from django import forms
from django.core.exceptions import ValidationError
from catalog.data import courses
import re

class TeacherForm(forms.Form):
    """Форма для добавления преподавателя"""
    
    # Поле ФИО - ОБЯЗАТЕЛЬНОЕ
    full_name = forms.CharField(
        label="ФИО преподавателя *",
        
        widget=forms.TextInput(attrs={
            'placeholder': 'Иванов Иван Иванович',
            'class': 'form-control',
            'style': 'width: 100%; padding: 8px; margin: 5px 0;'
        }),
        max_length=255,
        required=True,  # ОБЯЗАТЕЛЬНОЕ поле
        error_messages={
            'required': 'Поле "ФИО" обязательно для заполнения',
            'max_length': 'ФИО не может быть длиннее 255 символов'
        }
    )
    
    # Поле Email - ОБЯЗАТЕЛЬНОЕ
    email = forms.EmailField(
        label="Email адрес *",
        
        widget=forms.EmailInput(attrs={
            'placeholder': 'ivanov@example.com',
            'class': 'form-control',
            'style': 'width: 100%; padding: 8px; margin: 5px 0;'
        }),
        max_length=254,
        required=True,  # ОБЯЗАТЕЛЬНОЕ поле
        error_messages={
            'required': 'Поле "Email" обязательно для заполнения',
            'invalid': 'Введите корректный email адрес (например: name@domain.com)',
            'max_length': 'Email не может быть длиннее 254 символов'
        }
    )
    
    # Поле Телефон - НЕОБЯЗАТЕЛЬНОЕ, но с валидацией если заполнено
    phone = forms.CharField(
        label="Телефон",
        widget=forms.TextInput(attrs={
            'placeholder': '+7 (999) 123-45-67',
            'class': 'form-control',
            'style': 'width: 100%; padding: 8px; margin: 5px 0;'
        }),
        required=False,  # НЕОБЯЗАТЕЛЬНОЕ поле
        max_length=20
    )
    
    # Поле Биография - НЕОБЯЗАТЕЛЬНОЕ
    bio = forms.CharField(
        label="Биография",
        
        widget=forms.Textarea(attrs={
            'placeholder': 'Расскажите о преподавателе...',
            'class': 'form-control',
            'style': 'width: 100%; padding: 8px; margin: 5px 0; rows: 4;'
        }),
        required=False
    )
    
    # Поле Специализация - НЕОБЯЗАТЕЛЬНОЕ
    specialization = forms.CharField(
        label="Специализация",
        
        widget=forms.TextInput(attrs={
            'placeholder': 'Python, Django, JavaScript',
            'class': 'form-control',
            'style': 'width: 100%; padding: 8px; margin: 5px 0;'
        }),
        required=False
    )
    
    # Поле для выбора курсов - НЕОБЯЗАТЕЛЬНОЕ
    courses = forms.MultipleChoiceField(
        label="Курсы",
        help_text="Выберите курсы, которые ведет преподаватель (можно выбрать несколько)",
        widget=forms.SelectMultiple(attrs={
            'class': 'form-control',
            'style': 'width: 100%; padding: 8px; margin: 5px 0; height: 150px;'
        }),
        required=False
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Загружаем курсы из data.py
        from catalog.data import courses as course_data
        course_choices = [(str(course['id']), course['title']) for course in course_data]
        self.fields['courses'].choices = course_choices
    
    def clean_full_name(self):
        """Валидация ФИО"""
        full_name = self.cleaned_data.get('full_name', '').strip()
        
        # Проверка на пустую строку
        if not full_name:
            raise ValidationError('ФИО не может быть пустым')
        
        # Проверка на минимальную длину
        if len(full_name) < 3:
            raise ValidationError('ФИО должно содержать минимум 3 символа')
        
        # Проверка, что ФИО содержит только буквы, пробелы и дефисы
        if not re.match(r'^[а-яА-Яa-zA-Z\s\-]+$', full_name):
            raise ValidationError('ФИО может содержать только буквы, пробелы и дефисы')
        
        # Проверка, что ФИО содержит хотя бы два слова
        words = full_name.split()
        if len(words) < 2:
            raise ValidationError('Введите полное имя (имя и фамилию)')
        
        return full_name
    
    def clean_email(self):
        """Валидация email"""
        email = self.cleaned_data.get('email', '').strip().lower()
        
        # Проверка на пустую строку
        if not email:
            raise ValidationError('Email не может быть пустым')
        
        # Проверка на корректный формат email
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            raise ValidationError('Введите корректный email адрес')
        
        # Проверка на допустимые домены
        allowed_domains = ['gmail.com', 'yandex.ru', 'mail.ru', 'example.com', 'edu.ru']
        domain = email.split('@')[1] if '@' in email else ''
        
       
        return email
    
    def clean_phone(self):
        """Валидация номера телефона (только если поле заполнено)"""
        phone = self.cleaned_data.get('phone', '').strip()
        
        # Если поле пустое, пропускаем валидацию
        if not phone:
            return phone
        
        # Удаляем все нецифровые символы для проверки
        digits_only = re.sub(r'\D', '', phone)
        
        # Проверка длины номера
        if len(digits_only) < 10 or len(digits_only) > 15:
            raise ValidationError('Номер телефона должен содержать от 10 до 15 цифр')
        
        # Проверка формата номера (разрешаем различные форматы)
        # Форматы: +7 (999) 123-45-67, 8-999-123-45-67, 89991234567, +79991234567
        phone_patterns = [
            r'^\+?7[\s\-\(]?\d{3}[\s\-\)]?\d{3}[\s\-]?\d{2}[\s\-]?\d{2}$',  # Российские номера
            r'^8[\s\-]?\d{3}[\s\-]?\d{3}[\s\-]?\d{2}[\s\-]?\d{2}$',  # Российские номера с 8
            
        ]
        
        # Проверяем соответствует ли номер хотя бы одному паттерну
        is_valid = False
        for pattern in phone_patterns:
            if re.match(pattern, phone):
                is_valid = True
                break
        
        if not is_valid:
            raise ValidationError(
                'Неверный формат номера телефона. Используйте форматы: '
                '+7 (999) 123-45-67, 8-999-123-45-67 или 89991234567'
            )
        
        # Проверка, что номер не начинается с 0 (кроме кода страны)
        if digits_only.startswith('0') and not digits_only.startswith('07'):
            raise ValidationError('Номер телефона не может начинаться с 0')
        
        return phone
    
    def clean(self):
        """Общая валидация формы (для полей, зависящих друг от друга)"""
        cleaned_data = super().clean()
        
        full_name = cleaned_data.get('full_name')
        email = cleaned_data.get('email')
        
        # Пример: проверка, что email не содержит имя преподавателя
        if full_name and email:
            first_name = full_name.split()[0].lower() if full_name.split() else ''
            if first_name in email.lower():
                
            
                pass
        
        return cleaned_data