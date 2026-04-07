from django.db import models
from django.core.exceptions import ValidationError


class Teacher(models.Model):
    """Модель преподавателя"""
    first_name = models.CharField(
        max_length=50,
        verbose_name="Имя",
        db_index=True
    )
    last_name = models.CharField(
        max_length=50,
        verbose_name="Фамилия",
        db_index=True
    )
    patronymic = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Отчество"
    )
    email = models.EmailField(
        unique=True,
        verbose_name="Email",
        help_text="Уникальный email преподавателя"
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="Телефон"
    )
    hire_date = models.DateField(
        verbose_name="Дата найма"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Активен"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата обновления"
    )

    class Meta:
        verbose_name = "Преподаватель"
        verbose_name_plural = "Преподаватели"
        ordering = ['first_name', 'last_name', 'patronymic']
        unique_together = ['last_name', 'first_name', 'patronymic']

    @property
    def full_name(self):
        """Полное имя преподавателя"""
        if self.patronymic:
            return f"{self.last_name} {self.first_name} {self.patronymic}"
        return f"{self.last_name} {self.first_name}"

    def __str__(self):
        return self.full_name


class TeacherInfo(models.Model):
    """Дополнительная информация о преподавателе (связь 1:1)"""
    DEGREE_CHOICES = [
        ('assistant', 'Ассистент'),
        ('senior_lecturer', 'Старший преподаватель'),
        ('docent', 'Доцент'),
        ('professor', 'Профессор'),
    ]

    teacher = models.OneToOneField(
        Teacher,
        on_delete=models.CASCADE,  
        related_name='info',
        verbose_name="Преподаватель"
    )
    degree = models.CharField(
        max_length=20,
        choices=DEGREE_CHOICES,
        verbose_name="Ученая степень"
    )
    specialization = models.CharField(
        max_length=200,
        verbose_name="Специализация"
    )
    bio = models.TextField(
        blank=True,
        verbose_name="Биография"
    )
    office_number = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        verbose_name="Номер кабинета"
    )
    years_of_experience = models.PositiveIntegerField(
        default=0,
        verbose_name="Лет опыта"
    )

    class Meta:
        verbose_name = "Информация о преподавателе"
        verbose_name_plural = "Информация о преподавателях"

    def __str__(self):
        return f"Информация о {self.teacher}"


class Course(models.Model):
    """Модель курса (связь 1:N с Teacher)"""
    LEVEL_CHOICES = [
        ('beginner', 'Начальный'),
        ('intermediate', 'Средний'),
        ('advanced', 'Продвинутый'),
    ]

    title = models.CharField(
        max_length=200,
        unique=True,
        verbose_name="Название курса",
        db_index=True
    )
    description = models.TextField(
        verbose_name="Описание"
    )
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.SET_NULL, 
        null=True,
        blank=True,
        related_name='courses',
        verbose_name="Преподаватель"
    )
    level = models.CharField(
        max_length=20,
        choices=LEVEL_CHOICES,
        default='beginner',
        verbose_name="Уровень"
    )
    credits = models.PositiveIntegerField(
        default=3,
        verbose_name="Кредиты"
    )
    max_students = models.PositiveIntegerField(
        default=30,
        verbose_name="Максимум студентов"
    )
    start_date = models.DateField(
        verbose_name="Дата начала"
    )
    end_date = models.DateField(
        verbose_name="Дата окончания"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Активен"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания"
    )

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"

    def __str__(self):
        return self.title

    def clean(self):
        if self.start_date > self.end_date:
            raise ValidationError("Дата начала не может быть позже даты окончания")


class Student(models.Model):
    """Модель студента (связь N:N с Course)"""
    first_name = models.CharField(
        max_length=50,
        verbose_name="Имя",
        db_index=True
    )
    last_name = models.CharField(
        max_length=50,
        verbose_name="Фамилия",
        db_index=True
    )
    patronymic = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name="Отчество"
    )
    email = models.EmailField(
        unique=True,
        verbose_name="Email"
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name="Телефон"
    )
    date_of_birth = models.DateField(
        verbose_name="Дата рождения"
    )
    address = models.TextField(
        blank=True,
        verbose_name="Адрес"
    )
    enrollment_date = models.DateField(
        auto_now_add=True,
        verbose_name="Дата зачисления"
    )
    courses = models.ManyToManyField(
        Course,
        related_name='students',
        blank=True,
        verbose_name="Курсы"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Активен"
    )

    class Meta:
        verbose_name = "Студент"
        verbose_name_plural = "Студенты"
        ordering = ['first_name', 'last_name', 'patronymic']
        unique_together = ['first_name', 'last_name', 'patronymic']

    @property
    def full_name(self):
        """Полное имя студента"""
        if self.patronymic:
            return f"{self.last_name} {self.first_name} {self.patronymic}"
        return f"{self.last_name} {self.first_name}"

    def __str__(self):
        return self.full_name
    
    def get_available_courses(self):
        """Возвращает курсы, на которые студент еще не записан"""
        return Course.objects.exclude(id__in=self.courses.all())