from django.urls import path
from . import views


app_name="accounts"

urlpatterns = [
    path("register/", views.UserRegisterView.as_view(), name="user_register"),
    path("login/", views.UserLoginView.as_view(), name="user_login"),
    path("verify/", views.VerifyCodeView.as_view(), name="verify_code"),
    
    #API
    path("api/register/", views.UserRegisterAPIView.as_view(), name="user_register_api"),
    # path("api/login/", views.User)
   
]
