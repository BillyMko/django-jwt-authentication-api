from django.urls import path
from .views import RegisterView, ProfileView, LogoutView, VerifyEmailView, LoginView, PasswordResetRequestView, PasswordResetConfirmView, ResendVerificationView, AdminUserDetailView, AdminUserListView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView 

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='refresh-token'),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('testprofile/', ProfileView.as_view(), name='profile'),
    path('verify-email/', VerifyEmailView.as_view(), name="verify-email"),
    path('password-reset/request/', PasswordResetRequestView.as_view(),name="password-reset-request"),
    path('password-reset/confirm/', PasswordResetConfirmView.as_view(), name="password-reset-confirm"),
    path("resend-verification/", ResendVerificationView.as_view(), name="resend-verification"),
    path("admin/users/", AdminUserListView.as_view(), name="admin-users"),
    path("admin/users/<int:pk>/", AdminUserDetailView.as_view(), name="admin-user"),
    ]