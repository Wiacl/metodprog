from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class DjangoTestCaseAuthTests(TestCase):
    """Тесты с использованием Django TestCase и assertRedirects"""
    
    def setUp(self):
        """Создание тестового пользователя"""
        self.user = User.objects.create_user(
            username='djangotest',
            email='djangotest@example.com',
            password='testpass123',
            first_name='Django',
            last_name='Test'
        )
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.profile_url = reverse('profile')
        self.users_list_url = reverse('users_list')
    
    def test_register_redirects_to_profile(self):
        """Тест редиректа после регистрации с assertRedirects"""
        data = {
            'username': 'newdjango',
            'email': 'newdjango@example.com',
            'first_name': 'New',
            'last_name': 'Django',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!',
        }
        response = self.client.post(self.register_url, data)
        self.assertRedirects(response, self.profile_url)
    
    def test_login_redirects_to_profile(self):
        """Тест редиректа после входа с assertRedirects"""
        response = self.client.post(self.login_url, {
            'username': 'djangotest',
            'password': 'testpass123',
        })
        self.assertRedirects(response, self.profile_url)
    
    def test_logout_redirects_to_login(self):
        """Тест редиректа после выхода с assertRedirects"""
        self.client.login(username='djangotest', password='testpass123')
        response = self.client.post(self.logout_url)
        self.assertRedirects(response, '/accounts/login/')
    
    def test_unauthenticated_redirect_to_login(self):
        """Тест редиректа неавторизованного пользователя"""
        response = self.client.get(self.profile_url)
        self.assertRedirects(
            response, 
            f'{self.login_url}?next={self.profile_url}'
        )
    
    def test_login_authenticated_user_redirect(self):
        """Тест редиректа авторизованного со страницы входа"""
        self.client.login(username='djangotest', password='testpass123')
        response = self.client.get(self.login_url)
        self.assertRedirects(response, self.profile_url)
    
    def test_users_list_requires_auth(self):
        """Тест редиректа неавторизованного со списка пользователей"""
        response = self.client.get(self.users_list_url)
        self.assertRedirects(
            response,
            f'{self.login_url}?next={self.users_list_url}'
        )
    
    def test_password_reset_redirect(self):
        """Тест редиректа после запроса сброса пароля"""
        response = self.client.post(reverse('password_reset'), {
            'email': 'djangotest@example.com'
        })
        self.assertRedirects(response, '/accounts/password-reset/done/')
    
    def test_add_friend_redirect(self):
        """Тест редиректа после добавления друга"""
        friend = User.objects.create_user(
            username='friend',
            email='friend@example.com',
            password='testpass123'
        )
        self.client.login(username='djangotest', password='testpass123')
        response = self.client.post(
            reverse('add_friend', kwargs={'user_id': friend.id})
        )
        self.assertRedirects(
            response,
            reverse('user_detail', kwargs={'pk': friend.id})
        )
    
    def test_view_stranger_profile_forbidden(self):
        """Тест запрета просмотра профиля незнакомца"""
        stranger = User.objects.create_user(
            username='stranger',
            email='stranger@example.com',
            password='testpass123'
        )
        self.client.login(username='djangotest', password='testpass123')
        response = self.client.get(
            reverse('user_detail', kwargs={'pk': stranger.id})
        )
        self.assertEqual(response.status_code, 403)
    
    def test_register_invalid_data_no_redirect(self):
        """Тест отсутствия редиректа при невалидных данных"""
        data = {
            'username': '',
            'email': 'invalid',
            'first_name': '',
            'last_name': '',
            'password1': 'pass',
            'password2': 'different',
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(email='invalid').exists())