from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .serializers import UserRegisterSerializer, OtpCodeSerializer
from .models import User, Address
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
import random
from django.contrib import messages
from django.urls import reverse
from rest_framework.permissions import AllowAny
from django.conf import settings
import redis
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import JsonResponse
import json
from products.serializers import UserSerializer
from .serializers import AddressSerializer
from rest_framework import status
from orders.models import Order
from orders.serializers import OrderSerializer
# from .tasks import send_otp_email

# redis
redis_client = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)
from django.core.mail import send_mail

def send_otp_email(email, otp):
    subject = 'Your OTP Code'
    message = f'Your OTP code is: {otp}'
    from_email = 'mkalhor81126@gmail.com'
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)

class UserRegisterView(View):
    def get(self, request):
        return render(request, "accounts/register.html", {})
    
    
class VerifyCodeView(View):
     def get(self, request):
        return render(request, "accounts/verify_code.html", {})
    
    
    
class UserLoginView(View):
    def get(self, request):
        return render(request, "accounts/login.html", {})
    
    # def post(self, request):
    #     email = request.POST.get('email')
    #     password = request.POST.get('password')
    #     user = authenticate(request, email=email, password=password)
        
    #     if user is not None:
    #         login(request, user)
    #         # Redirect to a success page, or wherever you want
    #         messages.success(request, "You are logged in successfully", "success")
    #         return redirect("products:home")
    #     else:
    #         # Invalid login credentials
    #         messages.error(request, "Invalid email or password. Please try again.", "danger")
    #         return render(request, "accounts/login.html", {})
    
    

    


class CustomerPanelView(View):
    def get(self, request):
        return render(request, "accounts/customer_panel.html")
    
    
    
class CustomerAddressView(View):
    def get(self, request, address_id):
        return render(request, "accounts/customer_panel_address_edit.html")
    

class CustomerAddAddressView(View):
    def get(self, request):
        return render(request, "accounts/customer_panel_address_add.html")

class CustomerPanelEditView(View):
    def get(self, request):
        return render(request, "accounts/customer_panel_edit.html")    
    
    
    

    
class UserRegisterAPIView(APIView):
    """
    API view for registering a new user.

    This view handles the registration process for new users. It receives a POST request
    containing user registration data and validates it using the UserRegisterSerializer.
    If the data is valid, it generates a random OTP code, sends it to the user's phone number,
    and stores it in Redis for verification. It also stores the user's registration data in the
    session for later use. If the data is invalid, it returns appropriate error messages.

    Methods:
        post(request):
            Handles POST requests for user registration.
            Args:
                request (HttpRequest): The HTTP request object containing user registration data.

            Returns:
                HttpResponseRedirect: Redirects to the verification page if successful, or
                redirects back to the registration page with error messages if validation fails.
    """
    
    serializer_class = UserRegisterSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            random_code = random.randint(1000, 9999)
            send_otp_email(serializer.validated_data["email"], random_code)
            # OtpCode.objects.create(phone_number=serializer.validated_data["phone_number"], code=random_code)
            redis_client.setex(serializer.validated_data["email"], 180, random_code)
            request.session["user_profile_info"] = {
                "first_name":serializer.validated_data["first_name"],
                "last_name":serializer.validated_data["last_name"],
                "phone_number":serializer.validated_data["phone_number"],
                "email":serializer.validated_data["email"],
                "password":serializer.validated_data["password"]
            }
            return Response(status=status.HTTP_200_OK)
         
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
 
class VerifyCodeAPIView(APIView):
    """
    API view for verifying OTP code and completing user registration.

    This view handles the verification of the OTP code entered by the user during
    the registration process. If the OTP code is correct, it creates a new user
    using the provided registration data stored in the session. If the code is incorrect,
    it returns an error message. If the session data is missing or expired, it prompts
    the user to register again.

    Methods:
        post(request):
            Handles POST requests for verifying OTP code and completing user registration.
            Args:
                request (HttpRequest): The HTTP request object containing OTP code data.

            Returns:
                HttpResponseRedirect: Redirects to the login page if registration is successful,
                or redirects back to the verification page with error messages if verification fails.
    """
    serializer_class = OtpCodeSerializer

    def post(self, request):
        try:
            email = request.session["user_profile_info"]["email"]
        except KeyError:
            return Response(
                {"error": "Please register again"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            code = serializer.validated_data.get("code")
            if code == redis_client.get(email).decode('utf-8'):
                user_info = request.session.get("user_profile_info")
                try:
                    User.objects.create_user(
                        first_name=user_info["first_name"],
                        last_name=user_info["last_name"],
                        phone_number=user_info["phone_number"],
                        email=user_info["email"],
                        password=user_info["password"],
                    )
                    request.session.clear()
                    return Response(
                        {"message": "You are registered successfully",
                         "redirect_url": reverse("accounts:user_login")},
                        status=status.HTTP_200_OK
                    )
                except Exception as e:
                    return Response(
                        {"error": "Failed to register user", "detail": str(e)},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            else:
                return Response(
                    {"error": "Incorrect code"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                {"error": "Invalid input data"},
                status=status.HTTP_400_BAD_REQUEST
            )
        

    


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
        

        

 

class CustomerPanelAPIView(APIView):
    """
    API view for retrieving and updating customer information and addresses.

    This view provides GET and PUT methods for managing customer information and addresses.
    The GET method retrieves the current user's information and associated addresses.
    The PUT method updates the current user's information.

    Methods:
        get(request):
            Handles GET requests to retrieve customer information and addresses.
            Returns:
                Response: Returns customer information and addresses as JSON data.

        put(request):
            Handles PUT requests to update customer information.
            Returns:
                Response: Returns a success message and redirect URL if successful,
                or error messages if validation fails.
    """
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user_ser = UserSerializer(instance=request.user)
        addresses = Address.objects.filter(user=request.user)
        address_ser = AddressSerializer(instance=addresses, many=True)
        
        responses_data = {
            "customer_info":user_ser.data,
            "address_info":address_ser.data,
        }
        
        return Response(data=responses_data, status=status.HTTP_200_OK)
    
    def put(self, request):
        user_ser = UserSerializer(instance=request.user, data=request.data, partial=True)
        if user_ser.is_valid():
            user_ser.save()
        else:
            return Response(user_ser.errors, status=status.HTTP_400_BAD_REQUEST)

        redirect_url = reverse("accounts:user_panel")  
        return Response({'redirect_url': redirect_url}, status=status.HTTP_200_OK)
    

class EditAddressAPIView(APIView):
    """
    API view for retrieving and updating addresses.

    This view provides GET and PUT methods for managing addresses.
    The GET method retrieves information about a specific address.
    The PUT method updates the information of a specific address.

    Methods:
        get(request, address_id):
            Handles GET requests to retrieve information about a specific address.
            Args:
                address_id (int): The ID of the address to retrieve.
            Returns:
                Response: Returns the address information as JSON data if found,
                or a 404 error if the address does not exist.

        put(request, address_id):
            Handles PUT requests to update information about a specific address.
            Args:
                address_id (int): The ID of the address to update.
            Returns:
                Response: Returns a success message and redirect URL if successful,
                or error messages if validation fails.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = AddressSerializer
    def get(self, request, address_id):
        address = get_object_or_404(Address, pk=address_id)
        serializer = AddressSerializer(instance=address)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, address_id):
        address = get_object_or_404(Address, pk=address_id)
        serializer = AddressSerializer(instance=address, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            redirect_url = reverse("accounts:user_panel")  
            return Response({'redirect_url': redirect_url}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    



# class AddAddressAPIView(APIView):
#     permission_classes = [IsAuthenticated]
#     def post(self, request):
#         data = request.data
#         Address.objects.create(province=data['province'],
#                             city=data['city'],
#                             detailed_address=data['detailed_address'],
#                             postal_code=data['postal_code'],
#                             user=request.user)
#         return Response(status=status.HTTP_200_OK)
    
    

class AddAddressAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = AddressSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            Address.objects.create(province=data['province'],
                                city=data['city'],
                                detailed_address=data['detailed_address'],
                                postal_code=data['postal_code'],
                                user=request.user)
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    
class OrderHistoryApi(APIView):
    """
    API view for retrieving order history.

    This view provides GET method to retrieve the order history for the authenticated user.

    Attributes:
        permission_classes (list): List of permission classes required for accessing this view.

    Methods:
        get(request):
            Handles GET requests to retrieve order history for the authenticated user.
            Args:
                request (HttpRequest): The HTTP request object.
            Returns:
                Response: Returns the order history data as JSON data.
    """
    
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer
    def get(self, request):
        """
        Handles GET requests to retrieve order history for the authenticated user.
        """
        
        queryset = Order.objects.filter(user=request.user)
        serializer = OrderSerializer(queryset, many=True)
        return Response({'queryset': serializer.data})
    

class OrderHistory(View):
    def get(self, request):
        return render(request, "accounts/order_history.html")