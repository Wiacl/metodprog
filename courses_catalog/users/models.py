from django.db import models
from django.contrib.auth.models import AbstractUser
from PIL import Image
import logging

logger = logging.getLogger(__name__)


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
        full_name = f'{self.last_name} {self.first_name}'
        if self.middle_name:
            full_name += f' {self.middle_name}'
        return full_name
    
    def get_friends(self):
        return self.friends.all()
    
    def add_friend(self, user):
        if user != self:
            self.friends.add(user)
            user.friends.add(self)
    
    def remove_friend(self, user):
        self.friends.remove(user)
        user.friends.remove(self)
    
    def is_friend(self, user):
        return self.friends.filter(id=user.id).exists()
    
    def save(self, *args, **kwargs):
        """Переопределяем save для автоматического изменения размера аватара"""
        super().save(*args, **kwargs)
        
        if self.avatar:
            try:
                img = Image.open(self.avatar.path)
                
                # Максимальный размер аватара
                max_size = (300, 300)
                
                # Если изображение больше максимального размера - уменьшаем
                if img.height > max_size[1] or img.width > max_size[0]:
                    img.thumbnail(max_size, Image.Resampling.LANCZOS)
                    img.save(self.avatar.path, quality=85, optimize=True)
                    logger.info(
                        f"Avatar resized for user '{self.username}' "
                        f"to {img.size}"
                    )
                    
            except Exception as e:
                # Логируем ошибку с полным traceback
                logger.error(
                    f"Error processing avatar for user '{self.username}': {str(e)}",
                    exc_info=True
                )
                # Не глушим ошибку - пробрасываем дальше
                raise