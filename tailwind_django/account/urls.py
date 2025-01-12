from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings
from . import views
from django.conf import settings

app_name = 'account'

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('add_account/', views.add_account, name='add_account'),
    path('home/', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('accounts/', views.list_accounts, name='list_accounts'),
    path('accounts/<int:user_id>/delete/', views.delete_account, name='delete_account'),
    
    # Test Email URL
    path('test-email/', views.test_email, name='test_email'),
    
    # Account Management URLs
    path('manage/', views.manage_account, name='manage_account'),
    path('manage/update-display-name/', views.update_display_name, name='update_display_name'),
    path('manage/update-password/', views.update_password, name='update_password'),
    path('manage/update-email/', views.update_email, name='update_email'),
    
    # Password Reset URLs
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='account/password_reset.html',
        email_template_name='account/password_reset_email.html',
        subject_template_name='account/password_reset_subject.txt',
        success_url='/account/password_reset/done/',
        from_email=settings.EMAIL_HOST_USER
    ), name='password_reset'),
    
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='account/password_reset_done.html'
    ), name='password_reset_done'),
    
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='account/password_reset_confirm.html',
        success_url='/account/login/'
    ), name='password_reset_confirm'),
    
    path('reset/done/', views.CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
]