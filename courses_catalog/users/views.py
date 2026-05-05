from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.views.decorators.http import require_POST
from django.db.models import Q
from .forms import UserRegistrationForm, UserProfileForm
from .models import User


class RegisterView(CreateView):
    """
    Регистрация нового пользователя с автоматическим входом
    """
    form_class = UserRegistrationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('profile')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.object
        login(self.request, user)
        messages.success(self.request, f'Добро пожаловать, {user.get_full_name()}!')
        return response


@login_required
def profile_view(request):
    """
    Страница профиля текущего пользователя
    """
    return render(request, 'users/profile.html', {'user': request.user})


class UserProfileView(LoginRequiredMixin, DetailView):
    """
    Просмотр профиля пользователя
    """
    model = User
    template_name = 'users/user_detail.html'
    context_object_name = 'profile_user'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['is_friend'] = self.request.user.is_friend(self.object)
            context['can_view_full_profile'] = (
                self.object == self.request.user or 
                self.request.user.is_friend(self.object)
            )
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """
    Редактирование своего профиля
    """
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile_edit.html'
    success_url = reverse_lazy('profile')
    
    def get_object(self, queryset=None):
        return self.request.user
    
    def form_valid(self, form):
        messages.success(self.request, 'Профиль успешно обновлен!')
        return super().form_valid(form)


class UsersListView(LoginRequiredMixin, ListView):
    """
    Список всех пользователей с информацией о дружбе
    """
    model = User
    template_name = 'users/users_list.html'
    context_object_name = 'users'
    paginate_by = 20
    
    def get_queryset(self):
        # Исключаем текущего пользователя из списка
        return User.objects.exclude(id=self.request.user.id)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Создаем словарь с информацией о дружбе для каждого пользователя
        friends_dict = {}
        current_user = self.request.user
        
        for user in context['users']:
            friends_dict[user.id] = current_user.is_friend(user)
        
        context['friends_dict'] = friends_dict
        return context


@login_required
@require_POST
def add_friend(request, user_id):
    """
    Добавление пользователя в друзья
    """
    friend_user = get_object_or_404(User, id=user_id)
    
    if request.user == friend_user:
        messages.error(request, 'Вы не можете добавить себя в друзья')
        return redirect('users_list')
    
    if request.user.is_friend(friend_user):
        messages.info(request, f'{friend_user.get_full_name()} уже у вас в друзьях')
    else:
        request.user.add_friend(friend_user)
        messages.success(request, f'{friend_user.get_full_name()} добавлен(а) в друзья')
    
    # Перенаправляем обратно на ту страницу, откуда пришел запрос
    referer = request.META.get('HTTP_REFERER', '')
    if 'users/' in referer and referer != request.build_absolute_uri(request.path):
        return redirect(referer)
    return redirect('user_detail', pk=user_id)


@login_required
@require_POST
def remove_friend(request, user_id):
    """
    Удаление пользователя из друзей
    """
    friend_user = get_object_or_404(User, id=user_id)
    
    if request.user.is_friend(friend_user):
        request.user.remove_friend(friend_user)
        messages.success(request, f'{friend_user.get_full_name()} удален(а) из друзей')
    else:
        messages.info(request, f'{friend_user.get_full_name()} не в списке ваших друзей')
    
    # Перенаправляем обратно на ту страницу, откуда пришел запрос
    referer = request.META.get('HTTP_REFERER', '')
    if referer and referer != request.build_absolute_uri(request.path):
        return redirect(referer)
    return redirect('user_detail', pk=user_id)


@login_required
def friends_list(request):
    """
    Список друзей текущего пользователя
    """
    friends = request.user.get_friends()
    return render(request, 'users/friends_list.html', {'friends': friends})