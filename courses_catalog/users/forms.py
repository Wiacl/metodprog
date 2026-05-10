import logging
import re
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from PIL import Image
from .models import User

logger = logging.getLogger(__name__)


class UserRegistrationForm(UserCreationForm):
    """Форма для регистрации нового пользователя"""
    
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'example@mail.ru'
        })
    )
    
    first_name = forms.CharField(
        required=True,
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Иван'
        })
    )
    
    last_name = forms.CharField(
        required=True,
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Петров'
        })
    )
    
    middle_name = forms.CharField(
        required=False,
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Иванович (необязательно)'
        })
    )
    
    phone = forms.CharField(
        required=False,
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+7 (999) 123-45-67'
        })
    )
    
    class Meta:
        model = User
        fields = [
            'username', 'email', 'first_name', 'last_name', 
            'middle_name', 'phone', 'password1', 'password2'
        ]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Придумайте имя пользователя'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Придумайте пароль'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Повторите пароль'
        })
    
    def clean_phone(self):
        """Автоматически форматирует телефон"""
        phone = self.cleaned_data.get('phone', '').strip()
        
        if not phone:
            return phone
        
        digits = re.sub(r'\D', '', phone)
        
        if not digits:
            return phone
        
        try:
            if len(digits) >= 10:
                digits = digits[-10:]
                formatted = f'+7 ({digits[0:3]}) {digits[3:6]}-{digits[6:8]}-{digits[8:10]}'
            else:
                raise ValidationError('Номер телефона слишком короткий.')
            
            return formatted
            
        except (IndexError, ValueError):
            raise ValidationError('Ошибка при форматировании номера.')
    
    def clean_email(self):
        """Проверка уникальности email"""
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            logger.warning(f"Registration attempt with existing email: {email}")
            raise ValidationError('Пользователь с таким email уже существует')
        return email
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.middle_name = self.cleaned_data.get('middle_name', '')
        user.phone = self.cleaned_data.get('phone', '')
        
        if commit:
            user.save()
            logger.info(f"New user created: {user.username}")
        return user


class UserProfileForm(forms.ModelForm):
    """Форма для редактирования профиля пользователя"""
    
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'middle_name',
            'email', 'phone', 'avatar', 'bio'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'middle_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'avatar': forms.FileInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Расскажите о себе...'
            }),
        }
    
    def clean_avatar(self):
        """
        Проверка и обработка загружаемого аватара.
        Логирование ошибок с exc_info=True.
        """
        avatar = self.cleaned_data.get('avatar')
        
        if not avatar:
            return avatar
        
        # Проверка размера файла
        if avatar.size > 5 * 1024 * 1024:
            logger.warning(
                f"Avatar upload failed: file too large ({avatar.size} bytes) "
                f"for user '{self.instance.username}'"
            )
            raise ValidationError('Размер файла не должен превышать 5 МБ')
        
        # Проверка content_type
        allowed_content_types = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
        if hasattr(avatar, 'content_type') and avatar.content_type not in allowed_content_types:
            logger.warning(
                f"Avatar upload failed: invalid content type '{avatar.content_type}' "
                f"for user '{self.instance.username}'"
            )
            raise ValidationError(
                f'Неподдерживаемый тип файла. Разрешены: JPEG, PNG, GIF, WebP'
            )
        
        # Проверка, что файл действительно изображение
        try:
            img = Image.open(avatar)
            img.verify()
            
            # Переоткрываем после verify()
            img = Image.open(avatar)
            
            logger.info(
                f"Avatar validated for user '{self.instance.username}': "
                f"format={img.format}, size={img.size}"
            )
            
        except ValidationError:
            raise
        except Exception as e:
            logger.error(
                f"Error validating avatar for user '{self.instance.username}': {str(e)}",
                exc_info=True
            )
            raise ValidationError(
                'Ошибка при обработке изображения. Убедитесь, что файл не поврежден.'
            )
        
        return avatar
    
    def clean_phone(self):
        """Форматирование телефона"""
        phone = self.cleaned_data.get('phone', '').strip()
        
        if not phone:
            return phone
        
        digits = re.sub(r'\D', '', phone)
        
        if not digits:
            return phone
        
        try:
            if len(digits) >= 10:
                digits = digits[-10:]
                formatted = f'+7 ({digits[0:3]}) {digits[3:6]}-{digits[6:8]}-{digits[8:10]}'
            else:
                raise ValidationError('Номер телефона слишком короткий.')
            
            return formatted
            
        except (IndexError, ValueError):
            raise ValidationError('Ошибка при форматировании номера.')
