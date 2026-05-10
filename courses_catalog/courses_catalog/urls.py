from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import (
    PasswordChangeView,
    PasswordChangeDoneView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView
)
from django.shortcuts import redirect

# Импортируем кастомные view для входа/выхода
from users.auth_views import CustomLoginView, CustomLogoutView

from django.conf import settings
from django.conf.urls.static import static

def home_view(request):
    if request.user.is_authenticated:
        return redirect('profile')
    return redirect('login')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    
    path('schedule/', include('schedule.urls')),
    
    # Аутентификация с кастомными view
    path('accounts/login/', CustomLoginView.as_view(), name='login'),
    path('accounts/logout/', CustomLogoutView.as_view(), name='logout'),
    
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
    
    # Пользователи
    path('', include('users.urls')),
]

handler403 = 'users.views.custom_403'
handler404 = 'catalog.views.custom_404'

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)