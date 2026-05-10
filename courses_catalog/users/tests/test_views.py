import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.test import Client

User = get_user_model()


@pytest.fixture
def user(db):
    """Фикстура для создания обычного пользователя"""
    return User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123',
        first_name='Иван',
        last_name='Петров'
    )


@pytest.fixture
def user2(db):
    """Фикстура для создания второго пользователя"""
    return User.objects.create_user(
        username='testuser2',
        email='test2@example.com',
        password='testpass123',
        first_name='Петр',
        last_name='Иванов'
    )


@pytest.fixture
def client():
    """Фикстура для клиента"""
    return Client()


@pytest.fixture
def logged_client(client, user):
    """Фикстура для авторизованного клиента"""
    client.login(username='testuser', password='testpass123')
    return client


@pytest.mark.django_db
class TestRegistrationView:
    """Тесты регистрации"""
    
    def test_register_page_get(self, client):
        response = client.get(reverse('register'))
        assert response.status_code == 200
        assert 'form' in response.context
    
    def test_register_success(self, client):
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'first_name': 'Иван',
            'last_name': 'Петров',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!',
        }
        response = client.post(reverse('register'), data)
        assert response.status_code == 302
        assert User.objects.filter(username='newuser').exists()
        assert '_auth_user_id' in client.session
    
    def test_register_auto_login(self, client):
        data = {
            'username': 'newuser2',
            'email': 'newuser2@example.com',
            'first_name': 'Иван',
            'last_name': 'Петров',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!',
        }
        response = client.post(reverse('register'), data, follow=True)
        assert response.status_code == 200
        assert response.context['user'].is_authenticated
    
    @pytest.mark.parametrize('missing_field', [
        'username', 'email', 'first_name', 'last_name', 'password1', 'password2'
    ])
    def test_register_missing_fields(self, client, missing_field):
        data = {
            'username': 'newuser3',
            'email': 'newuser3@example.com',
            'first_name': 'Иван',
            'last_name': 'Петров',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!',
        }
        del data[missing_field]
        response = client.post(reverse('register'), data)
        assert response.status_code == 200


@pytest.mark.django_db
class TestLoginLogoutView:
    """Тесты входа и выхода"""
    
    def test_login_page_get(self, client):
        response = client.get(reverse('login'))
        assert response.status_code == 200
    
    def test_login_success(self, client, user):
        response = client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpass123',
        })
        assert response.status_code == 302
        assert response.url == reverse('profile')
    
    def test_login_invalid_credentials(self, client, user):
        response = client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'wrongpassword',
        })
        assert response.status_code == 200
    
    def test_logout(self, logged_client):
        response = logged_client.post(reverse('logout'))
        assert response.status_code == 302
    
    def test_login_authenticated_redirect(self, logged_client):
        response = logged_client.get(reverse('login'))
        assert response.status_code == 302


@pytest.mark.django_db
class TestProfileView:
    """Тесты профиля пользователя"""
    
    def test_profile_authenticated(self, logged_client):
        response = logged_client.get(reverse('profile'))
        assert response.status_code == 200
    
    def test_profile_unauthenticated(self, client):
        response = client.get(reverse('profile'))
        assert response.status_code == 302
    
    def test_profile_edit_get(self, logged_client):
        response = logged_client.get(reverse('profile_edit'))
        assert response.status_code == 200
    
    def test_profile_edit_post(self, logged_client, user):
        data = {
            'first_name': 'Петр',
            'last_name': 'Сидоров',
            'email': 'petr@example.com',
            'bio': 'Новая информация',
        }
        response = logged_client.post(reverse('profile_edit'), data)
        assert response.status_code == 302
        user.refresh_from_db()
        assert user.first_name == 'Петр'


@pytest.mark.django_db
class TestUserDetailView:
    """Тесты просмотра профиля пользователя"""
    
    def test_view_own_profile(self, logged_client, user):
        response = logged_client.get(reverse('user_detail', kwargs={'pk': user.id}))
        assert response.status_code == 200
    
    def test_view_friend_profile(self, logged_client, user, user2):
        user.add_friend(user2)
        response = logged_client.get(reverse('user_detail', kwargs={'pk': user2.id}))
        assert response.status_code == 200
    
    def test_view_stranger_profile(self, logged_client, user2):
        response = logged_client.get(reverse('user_detail', kwargs={'pk': user2.id}))
        assert response.status_code == 403


@pytest.mark.django_db
class TestFriendsView:
    """Тесты друзей"""
    
    def test_add_friend(self, logged_client, user, user2):
        response = logged_client.post(reverse('add_friend', kwargs={'user_id': user2.id}))
        assert response.status_code == 302
        assert user.is_friend(user2) is True
    
    def test_remove_friend(self, logged_client, user, user2):
        user.add_friend(user2)
        response = logged_client.post(reverse('remove_friend', kwargs={'user_id': user2.id}))
        assert response.status_code == 302
        assert user.is_friend(user2) is False
    
    def test_cannot_add_self(self, logged_client, user):
        response = logged_client.post(reverse('add_friend', kwargs={'user_id': user.id}))
        assert response.status_code == 302
    
    def test_friends_list(self, logged_client, user, user2):
        user.add_friend(user2)
        response = logged_client.get(reverse('friends_list'))
        assert response.status_code == 200
        assert len(response.context['friends']) == 1


@pytest.mark.django_db
class TestUsersListView:
    """Тесты списка пользователей"""
    
    def test_users_list_authenticated(self, logged_client, user, user2):
        response = logged_client.get(reverse('users_list'))
        assert response.status_code == 200
        assert user not in response.context['users']
        assert user2 in response.context['users']
    
    def test_users_list_unauthenticated(self, client):
        response = client.get(reverse('users_list'))
        assert response.status_code == 302


@pytest.mark.django_db
class TestAccessControl:
    """Тесты контроля доступа"""
    
    def test_anonymous_can_register(self, client):
        response = client.get(reverse('register'))
        assert response.status_code == 200
    
    def test_authenticated_redirect_from_login(self, logged_client):
        response = logged_client.get(reverse('login'))
        assert response.status_code == 302


@pytest.mark.django_db
class TestPasswordReset:
    """Тесты восстановления пароля"""
    
    def test_password_reset_get(self, client):
        response = client.get(reverse('password_reset'))
        assert response.status_code == 200
    
    def test_password_reset_post(self, client, user):
        response = client.post(reverse('password_reset'), {
            'email': 'test@example.com'
        })
        assert response.status_code == 302
