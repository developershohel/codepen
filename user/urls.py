from django.urls import path
from . import views
from django.views.generic import TemplateView

app_name = 'user'
urlpatterns = [
    path('login/', views.user_login, name="login_url"),
    path('signup/', views.signup, name="signup_url"),
    path('logout/', views.user_logout, name="logout_url"),
    path('auth/forgot-password/', views.forgot_password, name="forgot_password"),
    path('auth/change-password', views.change_password, name="change_password"),
    path('auth/change-password-token', views.change_password_token, name="change_password_token"),
    path('auth/change-password-code', views.change_password_code, name="change_password_code"),
    path('auth/change-password-resend-code', views.change_password_resend_code, name="change_password_resend_auth"),
    path('auth/verified-token', views.verified_token, name="auton_token"),
    path('auth/verified-code', views.verified_code, name="auton_code"),
    path('auth/verified-code-resend', views.verified_code_resend, name="verified_code_resend"),
    path('auth/user-validation', views.user_validation, name='user_validation')
]
