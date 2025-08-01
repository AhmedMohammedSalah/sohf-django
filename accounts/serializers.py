from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth import get_user_model

# [AMS]:- User Serializer for API representation
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = [
            'id', 'username', 'email', 'full_name',
            'phone_number', 'profile_picture'
            # 'is_quran_teacher', 'is_student' [AMS] for future role-based access control
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'profile_picture': {'required': False}
        }
    
    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            full_name=validated_data.get('full_name', ''),
            phone_number=validated_data.get('phone_number', ''),
            # is_quran_teacher=validated_data.get('is_quran_teacher', False),
            # is_student=validated_data.get('is_student', True)
        )
        return user

# [AMS]:- Login Serializer
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=128, write_only=True)

# [AMS]:- Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)
    
    class Meta:
        model = CustomUser
        fields = [
            'username', 'email', 'password', 'password2',
            'full_name', 'phone_number'
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("كلمات المرور غير متطابقة")
        return data
    
    def create(self, validated_data):
        validated_data.pop('password2')
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            full_name=validated_data.get('full_name', ''),
            phone_number=validated_data.get('phone_number', '')
        )
        return user