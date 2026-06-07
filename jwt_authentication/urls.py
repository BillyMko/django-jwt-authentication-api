from django.urls import path
from .views import RegisterView, ProfileView, LogoutView, VerifyEmailView, LoginView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView 

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='refresh-token'),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('testprofile/', ProfileView.as_view(), name='profile'),
    path('verify-email/<uuid:token>/', VerifyEmailView.as_view(), name="verify-email"),
]