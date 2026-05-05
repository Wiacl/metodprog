from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Кастомная модель пользователя с дополнительными полями
    """
    middle_name = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='Отчество'
    )
    
    phone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name='Телефон',
        help_text='В формате: +7 (999) 123-45-67'
    )
    
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True,
        verbose_name='Фото профиля'
    )
    
    bio = models.TextField(
        max_length=500,
        blank=True,
        verbose_name='О себе'
    )
    
    friends = models.ManyToManyField(
        'self',
        blank=True,
        verbose_name='Друзья'
    )
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['last_name', 'first_name']
    
    def __str__(self):
        if self.first_name and self.last_name:
            return f'{self.last_name} {self.first_name}'
        return self.username
    
    def get_full_name(self):
        """Возвращает полное имя пользователя"""
        full_name = f'{self.last_name} {self.first_name}'
        if self.middle_name:
            full_name += f' {self.middle_name}'
        return full_name
    
    def get_friends(self):
        """Возвращает список друзей"""
        return self.friends.all()
    
    def add_friend(self, user):
        """Добавляет пользователя в друзья"""
        if user != self:
            self.friends.add(user)
            user.friends.add(self)
    
    def remove_friend(self, user):
        """Удаляет пользователя из друзей"""
        self.friends.remove(user)
        user.friends.remove(self)
    
    def is_friend(self, user):
        """Проверяет, является ли пользователь другом"""
        return self.friends.filter(id=user.id).exists()