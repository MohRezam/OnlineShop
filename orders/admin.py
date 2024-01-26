from django.contrib import admin
from .models import Order, OrderItem, Coupon, Transaction, Cart, CartItem

# Register your models here.

admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Coupon)
admin.site.register(Transaction)