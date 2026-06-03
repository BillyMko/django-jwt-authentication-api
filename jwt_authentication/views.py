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


User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def perform_create(self, serializer):
        user = serializer.save()

        EmailVerificationToken.objects.create(user=user)




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
