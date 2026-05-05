from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Регистрация
    path('register/', views.RegisterView.as_view(), name='register'),
    
    # Профиль
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.ProfileUpdateView.as_view(), name='profile_edit'),
    
    # Пользователи
    path('users/', views.UsersListView.as_view(), name='users_list'),
    path('users/<int:pk>/', views.UserProfileView.as_view(), name='user_detail'),
    
    # Друзья
    path('friends/', views.friends_list, name='friends_list'),
    path('friends/add/<int:user_id>/', views.add_friend, name='add_friend'),
    path('friends/remove/<int:user_id>/', views.remove_friend, name='remove_friend'),
]