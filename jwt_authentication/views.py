from django.shortcuts import render
from .serializers import (
                          RegisterSerializer, 
                          LoginSerializer, 
                          RegisterSerializer, 
                          LogoutSerializer, 
                          PasswordResetConfirmSerializer, 
                          PasswordResetRequestSerializer, 
                          ProfileUpdateSerializer, 
                          AdminUserSerializer,
                          UserProfileSerializer
                          )
from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework  import status

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

from .models import EmailVerificationToken
from .emails import send_verification_email
from rest_framework.permissions import AllowAny

from .models import PasswordResetToken

from .permissions import IsAdmin, IsOwnerOrAdmin, IsPremium
 
from .passwordreset import send_password_reset_email
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

from .throttles import LoginRateThrottle, RegisterRateThrottle, PasswordResetRateThrottle

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    throttle_classes = [RegisterRateThrottle]

    def perform_create(self, serializer):
        user = serializer.save()

        verification_token_object = EmailVerificationToken.objects.create(user=user)

        send_verification_email(user, str(verification_token_object.token))

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        my_serializer = LogoutSerializer(data=request.data)
        my_serializer.is_valid(raise_exception=True)
        
        try:
            refresh_token = my_serializer.validated_data["refresh"]
            my_token = RefreshToken(refresh_token)
            my_token.blacklist()

            return Response (
                {"message": "Logged out successfully"},
                status=status.HTTP_200_OK
            )
        
        except TokenError:
            return Response(
                {"error": "Invalid or expired token"},
                status=status.HTTP_400_BAD_REQUEST
            )

class VerifyEmailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):

        try:
            token = request.query_params.get("token")
            token_obj = EmailVerificationToken.objects.get(token=token)

        except EmailVerificationToken.DoesNotExist:
            return Response(
                {"error": "Invalid verification token"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if token_obj.is_expired():
            token_obj.delete()
            return Response(
                {"error": "Token expired"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = token_obj.user
        user.is_verified = True
        user.save(update_fields=["is_verified"])

        token_obj.delete()

        return Response(
            {"message": "Email verified successfully"},
            status=status.HTTP_200_OK
        )
    

class LoginView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [LoginRateThrottle]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]
        refresh = RefreshToken.for_user(user)

        return Response ({
            "message": "Login successful",
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "email": user.email,
            "full name": user.full_name,
        })

class PasswordResetRequestView(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [PasswordResetRateThrottle]

    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]


        try:
            user = User.objects.get(email=email)
            PasswordResetToken.objects.filter(user=user, used = False).delete()
            reset_token = PasswordResetToken.objects.create(user=user)
            send_password_reset_email(user, reset_token.token)
            
        except User.DoesNotExist:
            pass

        return Response({"message":"If an account exists, a reset link has been sent to the email"},
                         status=status.HTTP_200_OK)
    

class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        
        serializer = PasswordResetConfirmSerializer(data=request.data, context={"token":request.query_params.get("token")})
        serializer.is_valid(raise_exception=True)

        reset_token = serializer.validated_data["reset_token"]
        new_password = serializer.validated_data["new_password"]
        user = reset_token.user

        user.set_password(new_password)
        user.save()

        reset_token.used =  True
        reset_token.save()

        return Response ({
            "message":
            "Password reset successful."

        },
        status=status.HTTP_200_OK
        )
    
class ResendVerificationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email", "").lower()

        if email == "":
            return Response(
                {"error":"Email is required"}, 
                status=status.HTTP_400_BAD_REQUEST
                )
        
        try:
            user = User.objects.get(email=email)
        
        except User.DoesNotExist:
            return Response(
                {"message":"If this email exists and not verified, a new verification link has been sent."},
                status=status.HTTP_200_OK
            )
        if user.is_verified:
            return Response(
                {"error":"Account already verified"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        EmailVerificationToken.objects.filter(user=user).delete()
        
        token_obj = EmailVerificationToken.objects.create(user=user)

        send_verification_email(user, str(token_obj.token))

        return Response(
            {"message":"A new verification email has been sent."},
            status=status.HTTP_200_OK
        )
    
class ProfileView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response (
            serializer.data
        )
    
    def patch(self, request):
        serializer = ProfileUpdateSerializer(request.user, data=request.data, partial=True, context={"request":request})
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            "message": "Profile updated successfully",
            "user": serializer.data
        })
    
class AdminUserListView(generics.ListAPIView):
    
    permission_classes = [IsAdmin]
    serializer_class = (AdminUserSerializer)

    def get_queryset(self):
        queryset = User.objects.all()
        role = self.request.query_params.get("role")
        is_verified = self.request.query_params.get("is_verified")
        search = self.request.query_params.get("search")

        if role:
            queryset = queryset.filter(role=role)
        
        if is_verified is not None:
            queryset = queryset.filter(is_verified=(is_verified.lower() == "true"))

        if search:
            from django.db.models import Q

            queryset = queryset.filter(

                    Q(email__icontains=search)
                    | 
                    Q(username__icontains=search)
                    | 
                    Q(first_name__icontains=search)
                    | 
                    Q(last_name__icontains=search)
            )
            
        return queryset
            
class AdminUserDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAdmin]
    serializer_class = (AdminUserSerializer)
    queryset = User.objects.all()
