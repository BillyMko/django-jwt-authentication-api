from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
User = get_user_model()

from django.contrib.auth.password_validation import validate_password

from .models import PasswordResetToken

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True)
    role = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'bio', 'password', 'confirm_password', 'role',]
        extra_kwargs = {"first_name":{"required": True}, "last_name":{"required": True}}

    def validate_email(self, value):
        value = value.lower()

        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists")
        
        return value

    def validate_username(self, value):

        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already taken.")
        
        return value

    def validate(self, data):
        if (data["password"] != data["confirm_password"]):
            raise serializers.ValidationError({"password": "Passwords do not match"})
        return data

    def create(self,validated_data):
        validated_data.pop("confirm_password")
        role = validated_data.pop("role", "user")
        if role == "admin":
            role = "user"
        user = User.objects.create_user(
            email = validated_data['email'],
            username=validated_data['username'], 
            password=validated_data['password'],
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", ""),
            bio=validated_data.get("bio", ""),
            role=role,
            is_verified = False
            )
       
        return user
    
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate_email(self, value):
        return value.lower()
    
    def validate(self, data):
        user = authenticate(
            email = data['email'],
            password=data['password']
        )
        if not user:
            raise serializers.ValidationError("Invalid credentials")

        if not user.is_verified:
            raise serializers.ValidationError("Please verify your email first.")
        
        if not user.is_active:
            raise serializers.ValidationError("Account has been deactivated")
        data['user'] = user
        return data
    
class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        return value.lower()

# class PasswordResetConfirmSerializer(serializers.Serializer):
#     token = serializers.UUIDField()

#     new_password = serializers.CharField(write_only=True, validators=[validate_password])

class PasswordResetConfirmSerializer(serializers.Serializer):
    # token = serializers.UUIDField()
    new_password = serializers.CharField(write_only=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):

        token = self.context.get("token")
        if not token:
            raise serializers.ValidationError("Token required")

        if data["new_password"] != data["confirm_password"]:
            raise serializers.ValidationError("Passwords do not match")
        
        try :
            reset_token = PasswordResetToken.objects.get(token=token)
        
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
                  "last_name",
                  "bio", 
                  "avatar",
                ]
    def validate_username(self, value):
        user = self.context["request"].user

        exists = (User.objects.filter(username=value).exclude(pk=user.pk).exists())
        if exists:
            raise serializers.ValidationError("Username already taken")
        
        return value
    
class AdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id", 
            "email",
            "first_name",
            "last_name",
            "role",
            "is_verified",
            "is_active",
            "date_joined"
        ]

    
class UserProfileSerializer(serializers.ModelSerializer):

    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id",
                    "username", 
                    "email", 
                    "first_name", 
                    "last_name", 
                    "full_name", 
                    "role", 
                    "is_verified", 
                    "bio", 
                    "avator",
                    "created_at",
                    "updated_at",
                    ]
        
        read_only_fields = [
            "id",
            "email",
            "role",
            "is_verified",
            "created_at",
            "updated_at",
        ]

    def get_full_name(self, obj):
        return (f"{obj.first_name} "
                f"{obj.last_name}").strip()
