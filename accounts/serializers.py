from rest_framework import serializers
from .models import User, OtpCode
from django.contrib import messages
from django.shortcuts import redirect

class UserRegisterSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    phone_number = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = User
        fields = ["first_name", "last_name", "phone_number", "email", "password"]
    
    
    # def validate_phone(self, value):
    #     if User.objects.filter(phone_number=value):
    #         raise serializers.ValidationError("This phone number is already in use")
    #     return value
    
    
    # def validate_email(self, value):
    #     if User.objects.filter(email=value).exists():  # Potential cause of recursion
    #         raise serializers.ValidationError("This email address is already in use.")
    #     return value
        
        
        
class OtpCodeSerializer(serializers.ModelSerializer):
    code = serializers.CharField(required=True)
    class Meta:
        model = OtpCode
        fields = ["code"]