import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.views.decorators.http import require_POST
from .forms import UserRegistrationForm, UserProfileForm
from .models import User

# Создаем логгер для этого модуля
logger = logging.getLogger(__name__)

def home_view(request):
    """
    Перенаправление на главную страницу.
    Если пользователь авторизован - на профиль,
    если нет - на страницу входа.
    """
    if request.user.is_authenticated:
        return redirect('profile')
    else:
        return redirect('login')
    
class RegisterView(CreateView):
    """Регистрация нового пользователя с автоматическим входом"""
    form_class = UserRegistrationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('profile')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.object
        login(self.request, user)
        
        # Логирование успешной регистрации
        logger.info(f"User '{user.username}' (email: {user.email}) successfully registered")
        
        messages.success(self.request, f'Добро пожаловать, {user.get_full_name()}!')
        return response
    
    def form_invalid(self, form):
        # Логирование ошибок регистрации
        errors = form.errors.as_json()
        logger.warning(f"Failed registration attempt. Errors: {errors}")
        return super().form_invalid(form)


@login_required
def profile_view(request):
    """Страница профиля текущего пользователя"""
    return render(request, 'users/profile.html', {'user': request.user})


class UserProfileView(LoginRequiredMixin, DetailView):
    """Просмотр профиля пользователя"""
    model = User
    template_name = 'users/user_detail.html'
    context_object_name = 'profile_user'
    
    def dispatch(self, request, *args, **kwargs):
        profile_user = self.get_object()
        
        if profile_user == request.user:
            return super().dispatch(request, *args, **kwargs)
        
        if request.user.is_friend(profile_user):
            logger.info(f"User '{request.user.username}' viewed friend '{profile_user.username}' profile")
            return super().dispatch(request, *args, **kwargs)
        
        # Логирование попытки доступа к чужому профилю
        logger.warning(
            f"User '{request.user.username}' attempted to view restricted profile of '{profile_user.username}'"
        )
        raise PermissionDenied('Вы не можете просматривать профиль этого пользователя.')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['is_friend'] = self.request.user.is_friend(self.object)
            context['is_own_profile'] = (self.object == self.request.user)
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """Редактирование своего профиля"""
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile_edit.html'
    success_url = reverse_lazy('profile')
    
    def get_object(self, queryset=None):
        return self.request.user
    
    def form_valid(self, form):
        # Логирование обновления профиля
        logger.info(f"User '{self.request.user.username}' updated their profile")
        messages.success(self.request, 'Профиль успешно обновлен!')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        # Логирование ошибок обновления профиля
        errors = form.errors.as_json()
        logger.warning(f"User '{self.request.user.username}' failed to update profile. Errors: {errors}")
        return super().form_invalid(form)


class UsersListView(LoginRequiredMixin, ListView):
    """Список всех пользователей"""
    model = User
    template_name = 'users/users_list.html'
    context_object_name = 'users'
    paginate_by = 20
    
    def get_queryset(self):
        return User.objects.exclude(id=self.request.user.id)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        friends_dict = {}
        current_user = self.request.user
        
        for user in context['users']:
            friends_dict[user.id] = current_user.is_friend(user)
        
        context['friends_dict'] = friends_dict
        return context


@login_required
@require_POST
def add_friend(request, user_id):
    """Добавление пользователя в друзья"""
    friend_user = get_object_or_404(User, id=user_id)
    
    if request.user == friend_user:
        logger.warning(f"User '{request.user.username}' tried to add themselves as friend")
        messages.error(request, 'Вы не можете добавить себя в друзья')
        return redirect('users_list')
    
    if request.user.is_friend(friend_user):
        logger.info(f"User '{request.user.username}' already friends with '{friend_user.username}'")
        messages.info(request, f'{friend_user.get_full_name()} уже у вас в друзьях')
    else:
        request.user.add_friend(friend_user)
        # Логирование добавления в друзья
        logger.info(f"User '{request.user.username}' added '{friend_user.username}' as friend")
        messages.success(request, f'{friend_user.get_full_name()} добавлен(а) в друзья')
    
    return redirect('user_detail', pk=user_id)


@login_required
@require_POST
def remove_friend(request, user_id):
    """Удаление пользователя из друзей"""
    friend_user = get_object_or_404(User, id=user_id)
    
    if request.user.is_friend(friend_user):
        request.user.remove_friend(friend_user)
        # Логирование удаления из друзей
        logger.info(f"User '{request.user.username}' removed '{friend_user.username}' from friends")
        messages.success(request, f'{friend_user.get_full_name()} удален(а) из друзей')
    else:
        logger.info(f"User '{request.user.username}' tried to remove non-friend '{friend_user.username}'")
        messages.info(request, f'{friend_user.get_full_name()} не в списке ваших друзей')
    
    return redirect('user_detail', pk=user_id)


@login_required
def friends_list(request):
    """Список друзей текущего пользователя"""
    friends = request.user.get_friends()
    return render(request, 'users/friends_list.html', {'friends': friends})


def custom_403(request, exception=None):
    """Кастомная страница для ошибки 403"""
    logger.warning(f"403 Forbidden for user '{request.user}' accessing {request.path}")
    return render(request, '403.html', status=403)