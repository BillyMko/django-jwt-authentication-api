from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
User = get_user_model()

from django.contrib.auth.password_validation import validate_password

from .models import PasswordResetToken

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6 )

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

    def create(self,validated_data):
        user = User.objects.create_user(
            email = validated_data['email'],
            username=validated_data['username'], 
            password=validated_data['password']
            )
        return user
    
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(
            email = data['email'],
            password=data['password']
        )
        if not user:
            raise serializers.ValidationError("Invalid credentials")

        # if not user.is_verified:
        #     raise serializers.ValidationError("Please verify your email first.")
        data['user'] = user
        return data
    
class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        return value.lower()

class PasswordResetConfirmSerializer(serializers.Serializer):
    token = serializers.UUIDField()

    new_password = serializers.CharField(write_only=True, validators=[validate_password])

class PasswordResetConfirmSerializer(serializers.Serializer):
    token = serializers.UUIDField()
    new_password = serializers.CharField(write_only=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):

        if data["new_password"] != data["confirm_password"]:
            raise serializers.ValidationError("Passwords do not match")
        
        try :
            reset_token = PasswordResetToken.objects.get(token=data["token"])
        
        except PasswordResetToken.DoesNotExist:
            raise serializers.ValidationError("Invalid reset token")
        
        if reset_token.is_valid() == False:
            raise serializers.ValidationError("Token expired or already used")
        
        data["reset_token"] = reset_token

        return data
        
class ProfileUpdateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ["username",
                  "first_name",
                  "last_name"
                ]
    def validate_username(self, value):
        user = self.context["request"].user

        exists = (User.objects.filter(username=value).exclude(pk=user.pk).exists())
        if exists:
            raise serializers.ValidationError("Username already taken")
        
        return value
    