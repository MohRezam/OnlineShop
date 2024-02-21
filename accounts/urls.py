from django.urls import path
from . import views


app_name="accounts"

urlpatterns = [
    path("register/", views.UserRegisterView.as_view(), name="user_register"),
    path("login/", views.UserLoginView.as_view(), name="user_login"),
    path("verify/", views.VerifyCodeView.as_view(), name="verify_code"),
    path("logout/", views.UserLogOutView.as_view(), name="user_logout"),
    
    #API
    path("api/register/", views.UserRegisterAPIView.as_view(), name="user_register_api"),
    path("api/verify/", views.VerifyCodeAPIView.as_view(), name="verify_code_api"),
    path("login/api/", views.LoginView.as_view(), name="user_login_api"),
   
]
