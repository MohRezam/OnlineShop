from typing import Any
from django.contrib.auth.base_user import AbstractBaseUser
from django.http import HttpRequest
from .models import User
from django.contrib.auth.backends import BaseBackend
# class PhoneBackend(BaseBackend):
#     def authenticate(self, request, username=None, password=None, **kwargs):
#         try:
#             user = User.objects.get(phone_number=username)
#             if user.check_password(password):
#                 return user
#             return None
#         except User.DoesNotExist:
#             return None    
    
    
#     def get_user(self, user_id):
#         try:
#             return User.objects.get(pk=user_id)
#         except User.DoesNotExist:
#             return None

class EmailBackend(BaseBackend):
    """
    Backend for authenticating users based on email address.

    This backend allows users to authenticate using their email address
    instead of a username. It checks if the provided email exists in the
    database and verifies the password.

    Methods:
        authenticate(request, username=None, password=None, **kwargs):
            Authenticates a user based on the provided email and password.
            Args:
                request: The HTTP request.
                username (str): The email address of the user.
                password (str): The password of the user.
                **kwargs: Additional keyword arguments.

            Returns:
                User: The authenticated user object if successful, None otherwise.

        get_user(user_id):
            Retrieves a user by their ID.
            Args:
                user_id (int): The ID of the user to retrieve.

            Returns:
                User: The user object if found, None otherwise.
    """
    
    
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
            return None
        except User.DoesNotExist:
            return None    
    
    
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
                