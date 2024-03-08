from rest_framework import serializers
from .models import User, Address
from django.contrib import messages
from django.shortcuts import redirect
import re
from djoser.serializers import UserSerializer as BaseUserSerializer, UserCreateSerializer as BaseUserCreateSerializer
from products.serializers import UserSerializer

class UserRegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for registering a new user.

    This serializer validates and processes user registration data, including
    the user's first name, last name, phone number, email, and password.

    Attributes:
        first_name (str): The first name of the user.
        last_name (str): The last name of the user.
        phone_number (str): The phone number of the user.
        email (str): The email address of the user.
        password (str): The password of the user.

    Methods:
        validate_phone_number(value):
            Validates the phone number to ensure it is unique and has the correct format.

        validate_email(value):
            Validates the email address to ensure it is unique.

        validate_password(value):
            Validates the password to ensure it meets the minimum length requirement.

    """
    
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    phone_number = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = User
        fields = ["first_name", "last_name", "phone_number", "email", "password"]
    
    
    def validate_phone_number(self, value):
        if User.objects.filter(phone_number=value):
            raise serializers.ValidationError("This phone number is already in use")
        elif len(value) < 11:
            raise serializers.ValidationError("Your phone number is not correct. Must be 11 digits long")
        return value
        
    
    
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():  
            raise serializers.ValidationError("This email address is already in use.")
        return value

    def validate_password(self, value):
        if len(value) < 6:
            raise serializers.ValidationError("Password must be at least 6 characters long")
        return value
        
        
# class UserLoginSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ["email", "password"]

#     def validate_email(self, value):
#         # Custom email validation logic
#         if not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", value):
#             raise serializers.ValidationError("Invalid email format")
#         return value

#     def validate_password(self, value):
#         # Add custom password validation logic here
#         # For example, you can check if the password meets certain criteria
#         if len(value) < 6:
#             raise serializers.ValidationError("Password must be at least 6 characters long")
#         return value


class OtpCodeSerializer(serializers.Serializer):
    """
    Serializer for validating OTP codes.

    This serializer validates the OTP code provided by the user.

    Attributes:
        code (str): The OTP code entered by the user.
    """
    code = serializers.CharField()
        


class UserCreateSerializer(BaseUserCreateSerializer):
    """
    Serializer for creating a new user.

    This serializer extends the BaseUserCreateSerializer and adds additional fields
    for creating a new user, including the user's phone number, email, password, first name, and last name.

    Attributes:
        id (int): The unique identifier of the user.
        phone_number (str): The phone number of the user.
        email (str): The email address of the user.
        password (str): The password of the user.
        first_name (str): The first name of the user.
        last_name (str): The last name of the user.
    """
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id', 'phone_number', 'email', 'password','first_name','last_name']
        


class AddressSerializer(serializers.ModelSerializer):
    """
    Serializer for address objects.

    This serializer is used to serialize address objects, including the province, city,
    detailed address, postal code, and whether the address belongs to an actual person.

    Attributes:
        id (int): The unique identifier of the address.
        province (str): The province of the address.
        city (str): The city of the address.
        detailed_address (str): The detailed address information.
        postal_code (int): The postal code of the address.
        is_actual_person (bool): Indicates if the address belongs to an actual person.
        user (UserSerializer): Serializer for the associated user object.
    """
    
    class Meta:
        model = Address
        fields = ["id", "province", "city", "detailed_address", "postal_code", "is_actual_person"]
    