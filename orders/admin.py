from django.contrib import admin
from .models import Order, OrderItem, Coupon, Transaction, Cart, CartItem

# Register your models here.

# admin.site.register(Order)
# admin.site.register(OrderItem)
# admin.site.register(Cart)
# admin.site.register(CartItem)
# admin.site.register(Coupon)
# admin.site.register(Transaction)




class OrderItemInline(admin.TabularInline):
    model = OrderItem
# @admin.register(OrderItem)
# class OrderItemAdmin(admin.ModelAdmin):
#     list_display = ('id', 'order', 'product', 'quantity')
#     date_hierarchy = "created_at"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'is_paid', 'created_at', 'updated_at')
    inlines = (OrderItemInline,)
    search_fields = ('id', 'user')
    list_filter = ('is_paid', 'created_at')
    ordering = ('-created_at',)
    date_hierarchy = "created_at"

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'updated_at')
    date_hierarchy = "created_at"

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'cart', 'product', 'quantity')
    date_hierarchy = "created_at"

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'percentage', 'expiration_date', 'available_quantity')
    search_fields = ('code',)
    list_filter = ('expiration_date',)
    ordering = ('-expiration_date',)

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'user', 'final_price','created_at')
    search_fields = ('id', 'final_price')
    list_filter = ('created_at',)
    ordering = ('-created_at',)