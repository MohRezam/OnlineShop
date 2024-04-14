from django.urls import path
from . import views


app_name="accounts"

urlpatterns = [
    path("register/", views.UserRegisterView.as_view(), name="user_register"),
    path("login/", views.UserLoginView.as_view(), name="user_login"),
    path("verify/", views.VerifyCodeView.as_view(), name="verify_code"),
    # path("logout/", views.UserLogOutView.as_view(), name="user_logout"),
    path("panel/", views.CustomerPanelView.as_view(), name="user_panel"),
    path("panel/edit/", views.CustomerPanelEditView.as_view(), name="user_panel_edit"),
    path("address/edit/<int:address_id>/", views.CustomerAddressView.as_view(), name="edit_address"),
    path("address/add/", views.CustomerAddAddressView.as_view(), name="add_address"),
    path('order_history/' , views.OrderHistory.as_view() , name="order_history"),
    
    #API
    path("register/api/v1/", views.UserRegisterAPIView.as_view(), name="user_register_api"),
    path("verify/api/v1/", views.VerifyCodeAPIView.as_view(), name="verify_code_api"),
    # path("login/api/", views.LoginView.as_view(), name="user_login_api"),
    path("panel/api/v1/", views.CustomerPanelAPIView.as_view(), name="user_panel_api"),
    path('address/edit/<int:address_id>/api/v1/', views.EditAddressAPIView.as_view(), name='edit_address_api_v1'),
    path('api/order_history/', views.OrderHistoryApi.as_view(), name='order_history_api'),
    path("address/add/api/v1/", views.AddAddressAPIView.as_view(), name="add_address_api"),
   
]

