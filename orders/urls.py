from django.urls import path
from . import views

app_name = "orders"

urlpatterns = [
    # path("create/", views.OrderCreateView.as_view(), name="order_create"),
    # path("detail/<int:order_id>/", views.OrderDetailView.as_view(), name="order_detail"),
    path("cart/", views.CartView.as_view(), name="cart"),
    path("cart/remove/<slug:product_slug>/", views.CartRemoveView.as_view(), name="cart_remove"),
    path("create/", views.OrderCreateView.as_view(), name="order_create"),
    path("detail/<int:order_id>/", views.OrderDetailView.as_view(), name="order_detail"),
    
    
    #APIs
    path("api/cart/<slug:slug>/", views.CartAPI.as_view(), name="cart_api"),
    path("api/order/<int:order_id>/", views.OrderAPIView.as_view(), name="order_api"),
]
