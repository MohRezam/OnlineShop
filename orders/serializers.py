from rest_framework import serializers
from .models import Order, OrderItem, Cart, CartItem, Coupon, Transaction
from products.serializers import ProductSerializer, UserSerializer



class CouponSerializer(serializers.ModelSerializer):
    """
    Serializer for the Coupon model.

    This serializer is used to convert Coupon model instances into JSON representations and vice versa.

    Attributes:
        code (str): The unique code for the coupon.

    Meta:
        model (Coupon): The Coupon model.
        fields (list): The fields to include in the serialized representation.
    """
    class Meta:
        model = Coupon
        fields = ['code']
        




class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer for the Order model.

    This serializer is used to convert Order model instances into JSON representations and vice versa.

    Attributes:
        user (UserSerializer): Serializer for the associated user.
        coupon (CouponSerializer): Serializer for the associated coupon.

    Meta:
        model (Order): The Order model.
        fields (list): The fields to include in the serialized representation.
    """
    
    user = UserSerializer()
    
    
    class Meta:
        model = Order
        fields = ['id', 'is_paid', 'user', 'calculate_total_price', 'created_at', 'province', 'city', 'detailed_address', 'postal_code']
        
    def calculate_total_price(self, obj):
        """
        Calculates the total price of the order.
        
        Args:
            obj (Order): The Order instance.
        
        Returns:
            Decimal: The total price of the order.
        """
        return obj.calculate_total_price()

class OrderItemSerializer(serializers.ModelSerializer):
    """
    Serializer for the OrderItem model.

    This serializer is used to convert OrderItem model instances into JSON representations and vice versa.

    Attributes:
        order (OrderSerializer): Serializer for the associated order.
        product (ProductSerializer): Serializer for the associated product.

    Meta:
        model (OrderItem): The OrderItem model.
        fields (list): The fields to include in the serialized representation.
    """
    
    order = OrderSerializer()
    product = ProductSerializer()
    
    
    class Meta:
        model = OrderItem
        fields = ['quantity', 'order', 'product']


class CartSerializer(serializers.ModelSerializer):
    """
    Serializer for the Cart model.

    This serializer is used to convert Cart model instances into JSON representations and vice versa.

    Attributes:
        user (UserSerializer): Serializer for the associated user.

    Meta:
        model (Cart): The Cart model.
        fields (list): The fields to include in the serialized representation.
    """
    
    user = UserSerializer()
    

    class Meta:
        model = Cart
        fields = ['created_at', 'user', 'calculate_total_price']
        
    def calculate_total_price(self, obj):
        """
        Calculates the total price of the cart.
        
        Args:
            obj (Cart): The Cart instance.
        
        Returns:
            Decimal: The total price of the cart.
        """
        return obj.calculate_total_price()
    
    
class CartItemSerializer(serializers.ModelSerializer):
    """
    Serializer for the CartItem model.

    This serializer is used to convert CartItem model instances into JSON representations and vice versa.

    Attributes:
        cart (CartSerializer): Serializer for the associated cart.
        product (ProductSerializer): Serializer for the associated product.

    Meta:
        model (CartItem): The CartItem model.
        fields (list): The fields to include in the serialized representation.
    """
    
    cart = CartSerializer()
    product = ProductSerializer()
    
    
    class Meta:
        model = CartItem
        fields = ['quantity', 'created_at', 'cart', 'product']
        


class TransactionSerializer(serializers.ModelSerializer):
    """
    Serializer for the Transaction model.

    This serializer is used to convert Transaction model instances into JSON representations and vice versa.

    Attributes:
        user (UserSerializer): Serializer for the associated user.
        order (OrderSerializer): Serializer for the associated order.

    Meta:
        model (Transaction): The Transaction model.
        fields (list): The fields to include in the serialized representation.
    """
    
    user = UserSerializer()
    order = OrderSerializer()
    
    
    class Meta:
        model = Transaction
        fields = ['final_price', 'transaction_type', 'user', 'order']