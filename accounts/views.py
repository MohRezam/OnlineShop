from django.shortcuts import render, redirect
from django.views import View
from .serializers import UserRegisterSerializer, OtpCodeSerializer
from .models import User, OtpCode
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
import random
from core.utils import send_otp_code
from django.contrib import messages

# Create your views here.


class UserRegisterView(View):
    def get(self, request):
        return render(request, "accounts/register.html", {})
    

class UserRegisterAPIView(APIView):
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.POST)
        if serializer.is_valid():
            random_code = random.randint(1000, 9999)
            send_otp_code(serializer.validated_data["phone_number"], random_code)
            OtpCode.objects.create(phone_number=serializer.validated_data["phone_number"], code=random_code)
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
        # error_message = serializer.errors.get('email')[0]  
        # return redirect('accounts:user_register', {'error_message': error_message})


class VerifyCodeView(APIView):
    def get(self, request):
        return render(request, "accounts/verify_code.html", {})
    
    def post(self, request):
        try:
            phone_number = request.session["user_profile_info"]["phone_number"]
        except:
            messages.error(request, "Please register again", "danger")
            return redirect("accounts:user_register")
            # return Response({"message":"User already registered"})
        otp_code_object = OtpCode.objects.get(phone_number=phone_number)
        serializer = OtpCodeSerializer(data=request.POST)
        
        if serializer.is_valid():
            if serializer.validated_data["code"] == str(otp_code_object.code):
                user_info = request.session["user_profile_info"]
                try:
                    User.objects.create_user(
                    first_name = user_info["first_name"],
                    last_name = user_info["last_name"],
                    phone_number = user_info["phone_number"],
                    email = user_info["email"],
                    password = user_info["password"],
                )   
                    otp_code_object.delete()
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
        return render(request, "accounts/login.html", {})
    
    
