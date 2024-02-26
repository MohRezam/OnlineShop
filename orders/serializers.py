from rest_framework import serializers
from .models import Order, OrderItem, Cart, CartItem, Coupon, Transaction
from products.serializers import ProductSerializer, UserSerializer



class CouponSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    
    
    class Meta:
        model = Coupon
        fields = ['code', 'percentage', 'expiration_date', 'available_quantity', 'usage_limit_per_user', 'is_active', 'user']
        




class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    coupon = CouponSerializer()
    
    
    class Meta:
        model = Order
        fields = ['id', 'is_paid', 'user', 'coupon']

class OrderItemSerializer(serializers.ModelSerializer):
    order = OrderSerializer()
    product = ProductSerializer()
    
    
    class Meta:
        model = OrderItem
        fields = ['quantity', 'order', 'product']


class CartSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    

    class Meta:
        model = Cart
        fields = ['created_at', 'user', 'calculate_total_price']
        
    def calculate_total_price(self, obj):
        return obj.calculate_total_price()
    
    
class CartItemSerializer(serializers.ModelSerializer):
    cart = CartSerializer()
    product = ProductSerializer()
    
    
    class Meta:
        model = CartItem
        fields = ['quantity', 'created_at', 'cart', 'product']
        


class TransactionSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    order = OrderSerializer()
    
    
    class Meta:
        model = Transaction
        fields = ['final_price', 'transaction_type', 'user', 'order']