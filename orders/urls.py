from django.urls import path
from . import views

app_name = "orders"

urlpatterns = [
    path("cart/", views.CartView.as_view(), name="cart"),
    path("cart/remove/<slug:product_slug>/", views.CartRemoveView.as_view(), name="cart_remove"),
    
    
    #APIs
    path("api/cart/<slug:slug>", views.CartAPI.as_view(), name="cart_api"),
]
