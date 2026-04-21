from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
import re


class Teacher(models.Model):
    """Модель преподавателя"""
    first_name = models.CharField(max_length=50, verbose_name="Имя", db_index=True)
    last_name = models.CharField(max_length=50, verbose_name="Фамилия", db_index=True)
    patronymic = models.CharField(max_length=50, blank=True, null=True, verbose_name="Отчество")
    
    # Н
    position = models.CharField(
        max_length=100,
        verbose_name="Должность",
        default="Преподаватель",
        choices=[
            ('assistant', 'Ассистент'),
            ('teacher', 'Преподаватель'),
            ('senior_teacher', 'Старший преподаватель'),
            ('docent', 'Доцент'),
            ('professor', 'Профессор'),
        ]
    )
    
    employee_id = models.CharField(
        max_length=20,
        unique=True,
        null=True, blank=True,
        verbose_name="Табельный номер",
        validators=[RegexValidator(r'^EMP-\d{6}$', 'Формат: EMP-123456')]
    )
    
    salary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True, blank=True,
        verbose_name="Зарплата",
        validators=[MinValueValidator(30000), MaxValueValidator(500000)]
    )
    
    work_experience_years = models.PositiveIntegerField(
        null=True, blank=True,
        verbose_name="Общий стаж работы (лет)",
        validators=[MinValueValidator(0), MaxValueValidator(60)]
    )
    
    rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        verbose_name="Рейтинг преподавателя",
        default=5.00,
        validators=[MinValueValidator(0.00), MaxValueValidator(5.00)]
    )
    
    # Существующие поля
    email = models.EmailField(unique=True, verbose_name="Email")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Телефон")
    hire_date = models.DateField(verbose_name="Дата найма")
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Преподаватель"
        verbose_name_plural = "Преподаватели"
        ordering = ['last_name', 'first_name']

    def __str__(self):
        if self.patronymic:
            return f"{self.last_name} {self.first_name} {self.patronymic}"
        return f"{self.last_name} {self.first_name}"


class TeacherInfo(models.Model):
    """Дополнительная информация о преподавателе"""
    DEGREE_CHOICES = [
        ('assistant', 'Ассистент'),
        ('senior_lecturer', 'Старший преподаватель'),
        ('docent', 'Доцент'),
        ('professor', 'Профессор'),
    ]
    
    teacher = models.OneToOneField(Teacher, on_delete=models.CASCADE, related_name='info')
    degree = models.CharField(max_length=20, choices=DEGREE_CHOICES, verbose_name="Ученая степень")
    specialization = models.CharField(max_length=200, verbose_name="Специализация")
    bio = models.TextField(blank=True, verbose_name="Биография")
    office_number = models.CharField(max_length=10, blank=True, null=True, verbose_name="Номер кабинета")
    years_of_experience = models.PositiveIntegerField(default=0, verbose_name="Лет опыта")
    
    # НОВЫЕ ПОЛЯ
    publications_count = models.PositiveIntegerField(
        default=0,
        null=True, blank=True,
        verbose_name="Количество публикаций",
        validators=[MaxValueValidator(500)]
    )
    
    scientific_degree_year = models.IntegerField(
        verbose_name="Год получения ученой степени",
        null=True,
        blank=True,
        validators=[MinValueValidator(1950), MaxValueValidator(2026)]
    )
    
    consulting_hours = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Часы консультаций",
        help_text="Например: Пн 14:00-16:00"
    )

    class Meta:
        verbose_name = "Информация о преподавателе"
        verbose_name_plural = "Информация о преподавателях"


class Course(models.Model):
    """Модель курса"""
    LEVEL_CHOICES = [
        ('beginner', 'Начальный'),
        ('intermediate', 'Средний'),
        ('advanced', 'Продвинутый'),
    ]
    
    title = models.CharField(max_length=200, unique=True, verbose_name="Название курса", db_index=True)
    description = models.TextField(verbose_name="Описание")
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True, related_name='courses')
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='beginner')
    credits = models.PositiveIntegerField(default=3, verbose_name="Кредиты")
    max_students = models.PositiveIntegerField(default=30, verbose_name="Максимум студентов")
    start_date = models.DateField(verbose_name="Дата начала")
    end_date = models.DateField(verbose_name="Дата окончания")
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    created_at = models.DateTimeField(auto_now_add=True)
    
    # НОВЫЕ ПОЛЯ
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Стоимость курса (руб)",
        default=0,
        validators=[MinValueValidator(0)]
    )
    
    duration_weeks = models.PositiveIntegerField(
        verbose_name="Длительность курса (недели)",
        default=16,
        validators=[MinValueValidator(1), MaxValueValidator(52)]
    )
    
    prerequisites = models.TextField(
        blank=True,
        verbose_name="Требования к слушателям",
        help_text="Что должен знать студент перед началом курса"
    )
    
    certificate_available = models.BooleanField(
        default=True,
        verbose_name="Выдается сертификат"
    )
    
    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"
        ordering = ['title']


class Student(models.Model):
    """Модель студента"""
    first_name = models.CharField(max_length=50, verbose_name="Имя", db_index=True)
    last_name = models.CharField(max_length=50, verbose_name="Фамилия", db_index=True)
    patronymic = models.CharField(max_length=50, blank=True, null=True, verbose_name="Отчество")
    email = models.EmailField(unique=True, verbose_name="Email")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Телефон")
    date_of_birth = models.DateField(verbose_name="Дата рождения")
    address = models.TextField(blank=True, verbose_name="Адрес")
    enrollment_date = models.DateField(auto_now_add=True, verbose_name="Дата зачисления")
    courses = models.ManyToManyField(Course, related_name='students', blank=True)
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    
    # Н
    student_id = models.CharField(
        null=True, blank=True,
        max_length=20,
        unique=True,
        verbose_name="Студенческий билет №",
        validators=[RegexValidator(r'^ST-\d{6}$', 'Формат: ST-123456')]
    )
    
    average_grade = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        default=0,
        verbose_name="Средний балл",
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    
    parent_phone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="Телефон родителей"
    )
    
    scholarship_amount = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0,
        verbose_name="Стипендия (руб)",
        validators=[MinValueValidator(0)]
    )
    
    class Meta:
        verbose_name = "Студент"
        verbose_name_plural = "Студенты"
        ordering = ['last_name', 'first_name']