from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
User = get_user_model()


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

        data['user'] = user
        return data


