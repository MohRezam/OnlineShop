from django.urls import path
from . import views

app_name = "orders"

urlpatterns = [
    path("cart/", views.CartView.as_view(), name="cart"),
    
    
    #APIs
    path("api/cart/<slug:slug>", views.CartAPI.as_view(), name="cart_api"),
]
