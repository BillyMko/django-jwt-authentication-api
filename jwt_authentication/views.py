from django.shortcuts import render
from .serializers import RegisterSerializer, LoginSerializer, RegisterSerializer, LogoutSerializer
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


User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def perform_create(self, serializer):
        user = serializer.save()

        verification_token_object = EmailVerificationToken.objects.create(user=user)

        send_verification_email(user, verification_token_object.token)



class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response ({
            'email':request.user.email,
            'username': request.user.username
        })

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

    def get(self, request, token):

        try:
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

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]
        refresh = RefreshToken.for_user(user)

        return Response ({
            "access": str(refresh.access_token),
            "refresh": str(refresh)
        })
