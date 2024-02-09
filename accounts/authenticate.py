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
                