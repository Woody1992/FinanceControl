from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

app_name = 'authentication'
urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('validate-username/', csrf_exempt(views.UsernameValidationView.as_view()), name='validate_username'),
    path('validate-email/', csrf_exempt(views.EmailValidationView.as_view()), name='validate_email'),
    path('activate/<uidb64>/<token>', views.VerificationView.as_view(), name='activate'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change_password'),
    path('password-reset/', views.RequestPasswordResetView.as_view(), name='request-password-reset'),
    path('password-reset-confirm/<uidb64>/<token>', views.PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
]
