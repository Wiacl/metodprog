import pytest
from django.contrib.auth import get_user_model
from users.forms import UserRegistrationForm, UserProfileForm

User = get_user_model()


@pytest.mark.django_db
class TestUserRegistrationForm:
    """Тесты формы регистрации"""
    
    @pytest.fixture
    def valid_data(self):
        """Фикстура с валидными данными для регистрации"""
        return {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'first_name': 'Иван',
            'last_name': 'Петров',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!',
        }
    
    def test_valid_form(self, valid_data):
        """Тест валидной формы"""
        form = UserRegistrationForm(data=valid_data)
        assert form.is_valid() is True
    
    def test_save_form(self, valid_data):
        """Тест сохранения формы"""
        form = UserRegistrationForm(data=valid_data)
        assert form.is_valid()
        user = form.save()
        assert user.username == 'newuser'
        assert user.email == 'newuser@example.com'
        assert user.first_name == 'Иван'
        assert user.last_name == 'Петров'
    
    @pytest.mark.parametrize('field,value,expected_error', [
        ('username', '', 'Обязательное поле'),
        ('email', '', 'Обязательное поле'),
        ('email', 'invalid-email', 'Введите правильный адрес электронной почты'),
        ('first_name', '', 'Обязательное поле'),
        ('last_name', '', 'Обязательное поле'),
        ('password2', 'DifferentPass123!', 'Введенные пароли не совпадают'),
    ])
    def test_invalid_fields(self, valid_data, field, value, expected_error):
        """Параметризованный тест невалидных полей"""
        test_data = valid_data.copy()
        test_data[field] = value
        form = UserRegistrationForm(data=test_data)
        assert form.is_valid() is False
        assert field in form.errors
    
    def test_duplicate_username(self, valid_data):
        """Тест дублирующегося username"""
        User.objects.create_user(
            username='newuser',
            email='existing@example.com',
            password='testpass123'
        )
        form = UserRegistrationForm(data=valid_data)
        assert form.is_valid() is False
        assert 'username' in form.errors
    
    def test_duplicate_email(self, valid_data):
        """Тест дублирующегося email"""
        User.objects.create_user(
            username='existing',
            email='newuser@example.com',
            password='testpass123'
        )
        form = UserRegistrationForm(data=valid_data)
        assert form.is_valid() is False
        assert 'email' in form.errors
    
    def test_phone_formatting(self):
        """Тест форматирования телефона"""
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'first_name': 'Иван',
            'last_name': 'Петров',
            'phone': '89991234567',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!',
        }
        form = UserRegistrationForm(data=data)
        assert form.is_valid()
        user = form.save()
        assert user.phone == '+7 (999) 123-45-67'
    
    @pytest.mark.parametrize('phone_input,expected', [
        ('+7 (999) 123-45-67', '+7 (999) 123-45-67'),
        ('+79991234567', '+7 (999) 123-45-67'),
        ('89991234567', '+7 (999) 123-45-67'),
        ('9991234567', '+7 (999) 123-45-67'),
        
    ])
    def test_phone_format_variants(self, phone_input, expected):
        """Параметризованный тест разных форматов телефона"""
        data = {
            'username': f'testuser_{phone_input[-4:]}',
            'email': f'test_{phone_input[-4:]}@example.com',
            'first_name': 'Иван',
            'last_name': 'Петров',
            'phone': phone_input,
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!',
        }
        form = UserRegistrationForm(data=data)
        assert form.is_valid()
        user = form.save()
        assert user.phone == expected