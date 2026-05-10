import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
class TestUserModel:
    """Тесты для кастомной модели пользователя"""
    
    def test_create_user(self):
        """Тест создания обычного пользователя"""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Иван',
            last_name='Петров'
        )
        assert user.username == 'testuser'
        assert user.email == 'test@example.com'
        assert user.first_name == 'Иван'
        assert user.last_name == 'Петров'
        assert user.is_active is True
        assert user.is_staff is False
        assert user.is_superuser is False
    
    def test_create_superuser(self):
        """Тест создания суперпользователя"""
        admin = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123'
        )
        assert admin.is_superuser is True
        assert admin.is_staff is True
    
    def test_get_full_name(self):
        """Тест метода get_full_name"""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Иван',
            last_name='Петров',
            middle_name='Иванович'
        )
        assert user.get_full_name() == 'Петров Иван Иванович'
    
    def test_add_friend(self):
        """Тест добавления в друзья"""
        user1 = User.objects.create_user(
            username='user1',
            email='user1@example.com',
            password='testpass123'
        )
        user2 = User.objects.create_user(
            username='user2',
            email='user2@example.com',
            password='testpass123'
        )
        
        user1.add_friend(user2)
        assert user1.is_friend(user2) is True
        assert user2.is_friend(user1) is True
    
    def test_remove_friend(self):
        """Тест удаления из друзей"""
        user1 = User.objects.create_user(
            username='user1',
            email='user1@example.com',
            password='testpass123'
        )
        user2 = User.objects.create_user(
            username='user2',
            email='user2@example.com',
            password='testpass123'
        )
        
        user1.add_friend(user2)
        user1.remove_friend(user2)
        assert user1.is_friend(user2) is False
        assert user2.is_friend(user1) is False