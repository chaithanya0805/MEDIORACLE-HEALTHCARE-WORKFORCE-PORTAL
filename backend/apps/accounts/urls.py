from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from apps.accounts.views import CustomLoginView, RegisterView, MeView, LogoutView, ChangePasswordView, ForgotPasswordView, ResetPasswordView

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='auth_login'),
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='auth_logout'),
    path('me/', MeView.as_view(), name='auth_me'),
    path('change-password/', ChangePasswordView.as_view(), name='auth_change_password'),
    path('forgot-password/', ForgotPasswordView.as_view(), name='auth_forgot_password'),
    path('reset-password/', ResetPasswordView.as_view(), name='auth_reset_password'),
]
