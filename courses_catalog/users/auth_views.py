import logging
from django.contrib.auth import views as auth_views
from django.contrib import messages
from django.shortcuts import redirect

logger = logging.getLogger(__name__)


class CustomLoginView(auth_views.LoginView):
    """
    Кастомная view для входа с логированием
    """
    template_name = 'registration/login.html'
    redirect_authenticated_user = True
    
    def form_valid(self, form):
        """Успешный вход"""
        username = form.cleaned_data.get('username')
        logger.info(f"User '{username}' successfully logged in")
        messages.success(self.request, f'Добро пожаловать, {username}!')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        """Неудачный вход"""
        username = form.cleaned_data.get('username', 'unknown')
        logger.warning(f"Failed login attempt for user '{username}'")
        messages.error(self.request, 'Неверное имя пользователя или пароль.')
        return super().form_invalid(form)


class CustomLogoutView(auth_views.LogoutView):
    """
    Кастомная view для выхода с логированием
    """
    template_name = 'registration/logged_out.html'
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            logger.info(f"User '{request.user.username}' logged out")
        return super().dispatch(request, *args, **kwargs)