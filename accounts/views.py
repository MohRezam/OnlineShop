from django.shortcuts import render, redirect
from django.views import View
from .serializers import UserRegisterSerializer, OtpCodeSerializer
from .models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
import random
from core.utils import send_otp_code
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from rest_framework.permissions import AllowAny
from django.conf import settings
import redis

# redis
redis_client = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)


class UserRegisterView(View):
    def get(self, request):
        return render(request, "accounts/register.html", {})
    

class UserRegisterAPIView(APIView):
    # permission_classes = [AllowAny, ]
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.POST)
        if serializer.is_valid():
            random_code = random.randint(1000, 9999)
            send_otp_code(serializer.validated_data["phone_number"], random_code)
            # OtpCode.objects.create(phone_number=serializer.validated_data["phone_number"], code=random_code)
            redis_client.setex(serializer.validated_data["phone_number"], 180, random_code)
            phone_number = serializer.validated_data["phone_number"]
            hidden_phone_number = phone_number[:2] + '*'*(len(phone_number)-4) + phone_number[-2:]
            request.session["user_profile_info"] = {
                "first_name":serializer.validated_data["first_name"],
                "last_name":serializer.validated_data["last_name"],
                "phone_number":serializer.validated_data["phone_number"],
                "email":serializer.validated_data["email"],
                "password":serializer.validated_data["password"]
            }
            messages.success(request, f"we sent {hidden_phone_number} a code", 'success')
            return redirect('accounts:verify_code')
        error_messages = serializer.errors
        for k, v in error_messages.items():
            message = v[0]
        messages.error(request, f"{message}", "danger")  
        return redirect('accounts:user_register')
    
class VerifyCodeView(View):
     def get(self, request):
        return render(request, "accounts/verify_code.html", {})
class VerifyCodeAPIView(APIView): 
    def post(self, request):
        try:
            phone_number = request.session["user_profile_info"]["phone_number"]
        except:
            messages.error(request, "Please register again", "danger")
            return redirect("accounts:user_register")
            # return Response({"message":"User already registered"})
        # otp_code_object = OtpCode.objects.get(phone_number=phone_number)
        serializer = OtpCodeSerializer(data=request.POST)
        
        if serializer.is_valid():
            # if serializer.validated_data["code"] == str(otp_code_object.code):
            if redis_client.get(phone_number).decode('utf-8') == serializer.validated_data["code"]:
                user_info = request.session["user_profile_info"]
                try:
                    User.objects.create_user(
                    first_name = user_info["first_name"],
                    last_name = user_info["last_name"],
                    phone_number = user_info["phone_number"],
                    email = user_info["email"],
                    password = user_info["password"],
                )   
                    # otp_code_object.delete()
                    request.session.clear()
                    messages.success(request, "You registered successfuly")
                    return redirect("accounts:user_login")
                    # return Response({"message":"user registered successfuly"})
                except:
                    messages.error(request, "You are already registered", "danger")
                    return redirect("accounts:user_login")
                    # return Response({"message": "User already registered"})
            messages.error(request, "Code is not correct", "danger")
            return redirect("accounts:verify_code")
        return redirect(request, "accounts:user_login")
        # return Response(serializer.errors)
class UserLoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            messages.info(request, "You are already logged in.")
            return redirect("products:home")
        return render(request, "accounts/login.html", {})
    
    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            login(request, user)
            # Redirect to a success page, or wherever you want
            messages.success(request, "You are logged in successfully", "success")
            return redirect("products:home")
        else:
            # Invalid login credentials
            messages.error(request, "Invalid email or password. Please try again.", "danger")
            return render(request, "accounts/login.html", {})
    
    
        

# class UserLoginAPIView(APIView):
#     def post(self, request):
#         email = request.POST["email"]
#         password = request.POST["password"]
        
#         user = authenticate(request, username=email, password=password)
#         if user is not None:
#             user.is_active = True
#             user.save(update_fields=["is_active"])
#             login(request, user)
#             messages.success(request, "Logged in successfully")
#             return redirect("products:home")
#         else:
#             messages.error(request, "Invalid email or password")
#             return redirect("accounts:user_login")
        

        
class UserLogOutView(View):
    def get(self, request):
        if request.user.is_authenticated:
            user = request.user
            logout(request)
            messages.success(request, "You logged out successfully", "success")
        return redirect("products:home")