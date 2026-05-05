from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import (
    LoginView, 
    LogoutView,
    PasswordChangeView,
    PasswordChangeDoneView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('catalog.urls')),
    path('schedule/', include('schedule.urls')),
    
    # Аутентификация (префикс 'accounts/' как у вас было)
    path('accounts/login/', LoginView.as_view(
        template_name='registration/login.html',
        redirect_authenticated_user=True
    ), name='login'),
    path('accounts/logout/', LogoutView.as_view(
        template_name='registration/logged_out.html'
    ), name='logout'),
    path('accounts/password-change/', PasswordChangeView.as_view(
        template_name='registration/password_change_form.html',
        success_url='/accounts/password-change/done/'
    ), name='password_change'),
    path('accounts/password-change/done/', PasswordChangeDoneView.as_view(
        template_name='registration/password_change_done.html'
    ), name='password_change_done'),
    path('accounts/password-reset/', PasswordResetView.as_view(
        template_name='registration/password_reset_form.html',
        email_template_name='registration/password_reset_email.html',
        subject_template_name='registration/password_reset_subject.txt',
        success_url='/accounts/password-reset/done/'
    ), name='password_reset'),
    path('accounts/password-reset/done/', PasswordResetDoneView.as_view(
        template_name='registration/password_reset_done.html'
    ), name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
        template_name='registration/password_reset_confirm.html',
        success_url='/accounts/reset/done/'
    ), name='password_reset_confirm'),
    path('accounts/reset/done/', PasswordResetCompleteView.as_view(
        template_name='registration/password_reset_complete.html'
    ), name='password_reset_complete'),
    
    # Регистрация и профили пользователей
    path('', include('users.urls')),
]

handler404 = 'catalog.views.custom_404'