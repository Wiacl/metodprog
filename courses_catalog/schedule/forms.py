# schedule/forms.py
from django import forms
from catalog.data import courses

class TeacherForm(forms.Form):
    """Форма для добавления преподавателя"""
    full_name = forms.CharField(
        label="ФИО преподавателя",
        help_text="Введите полное имя преподавателя",
        widget=forms.TextInput(attrs={
            'placeholder': 'Иванов Иван Иванович',
            'class': 'form-control',
            'style': 'width: 100%; padding: 8px; margin: 5px 0;'
        }),
        max_length=255
    )
    
    email = forms.EmailField(
        label="Email адрес",
        help_text="Введите действующий email адрес",
        widget=forms.EmailInput(attrs={
            'placeholder': 'ivanov@example.com',
            'class': 'form-control',
            'style': 'width: 100%; padding: 8px; margin: 5px 0;'
        }),
        required=False,  # Сделаем необязательным, так как в data.py нет email
        max_length=254
    )
    
    phone = forms.CharField(
        label="Телефон",
        help_text="Необязательное поле. Введите номер телефона",
        widget=forms.TextInput(attrs={
            'placeholder': '+7 (999) 123-45-67',
            'class': 'form-control',
            'style': 'width: 100%; padding: 8px; margin: 5px 0;'
        }),
        required=False,
        max_length=20
    )
    
    bio = forms.CharField(
        label="Биография",
        help_text="Краткая биография преподавателя",
        widget=forms.Textarea(attrs={
            'placeholder': 'Расскажите о преподавателе...',
            'class': 'form-control',
            'style': 'width: 100%; padding: 8px; margin: 5px 0; rows: 4;'
        }),
        required=False
    )
    
    specialization = forms.CharField(
        label="Специализация",
        help_text="Область специализации преподавателя",
        widget=forms.TextInput(attrs={
            'placeholder': 'Python, Django, JavaScript',
            'class': 'form-control',
            'style': 'width: 100%; padding: 8px; margin: 5px 0;'
        }),
        required=False
    )
    
    # Поле для выбора курсов
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
        from catalog.data import courses
        course_choices = [(str(course['id']), course['title']) for course in courses]
        self.fields['courses'].choices = course_choices