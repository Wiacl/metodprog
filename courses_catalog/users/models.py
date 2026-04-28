from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class User(AbstractUser):
    """
    Кастомная модель пользователя
    Расширяет стандартную модель Django
    """
    
    # Дополнительные поля
    middle_name = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Отчество"
    )
    
    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="Телефон"
    )
    
    birth_date = models.DateField(
        blank=True,
        null=True,
        verbose_name="Дата рождения"
    )
    
    # Роли пользователей
    ROLE_CHOICES = [
        ('student', 'Студент'),
        ('teacher', 'Преподаватель'),
        ('admin', 'Администратор'),
    ]
    
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='student',
        verbose_name="Роль"
    )
    
    # Связь с моделью Teacher (если пользователь - преподаватель)
    teacher_profile = models.OneToOneField(
        'schedule.Teacher',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='user_account',
        verbose_name="Профиль преподавателя"
    )
    
    # Связь с моделью Student (если пользователь - студент)
    student_profile = models.OneToOneField(
        'schedule.Student',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='user_account',
        verbose_name="Профиль студента"
    )
    
    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
    
    def __str__(self):
        return self.get_full_name() or self.username