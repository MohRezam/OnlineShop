from django.db import models
from core.models import BaseModel
from accounts.models import User
from products.models import Product
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
# def create_order_from_cart(self, cart): # this cart is an object of Cart model  # fekr konam in ye method dar dakel order bayad bashe not so sure.
#     order = self.create(user=cart.user, total_price=cart.calculate_total_price())

#     for cart_item in cart.cart_items.all():
#         OrderItem.objects.create(order=order, product=cart_item.product, quantity=cart_item.quantity)

#     cart.delete()

#     return order

class Order(BaseModel):
    """
    Model for representing orders placed by users.

    This model stores information about orders, including payment status, delivery details,
    and associated user and coupon.

    Attributes:
        PAYMENT_CHOICES (tuple): Choices for the payment status of the order.
        is_paid (str): Indicates whether the order has been paid.
        province (str): The province for delivery.
        city (str): The city for delivery.
        detailed_address (str): Detailed address for delivery.
        postal_code (int): The postal code for delivery.
        user (ForeignKey): Reference to the user who placed the order.
        coupon (ForeignKey): Reference to the coupon applied to the order.

    Methods:
        __str__():
            Returns a string representation of the order.
        
        calculate_total_price():
            Calculates the total price of the order.

    Meta:
        verbose_name_plural (str): Plural name for the model in the admin interface.
    """
    
    PAYMENT_CHOICES = (
        ("not paid", "Not Paid"),
        ("paid", "Paid"),
    )
    # total_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.CharField(max_length=25, choices=PAYMENT_CHOICES, default=False) # when we create order from cart we have to set is_paid to True
    province = models.CharField(max_length=255, blank=True, null=True, help_text="like Alborz") # if user dont fill this it is going to fill by user address model informations
    city = models.CharField(max_length=255, blank=True, null=True, help_text="like karaj")
    detailed_address = models.TextField(blank=True, null=True)
    postal_code = models.PositiveIntegerField(blank=True, null=True, help_text="like 3149757953")
    discount = models.IntegerField(blank=True, null=True, default=None)
    # max_discount = models.IntegerField(blank=True, null=True, default=None)

    # Foreign Keys
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    
    def __str__(self) -> str:
        return f"Total: {self.calculate_total_price()}, Payment: {self.is_paid}"
    
    
    def calculate_total_price(self):
        total = sum(item.total_price() for item in self.order_items.all())
        if self.discount:
            discount_price = (self.discount / 100) * float(total)
            # if self.max_discount != None and discount_price > self.max_discount:
            #     return int(float(total) - self.max_discount)
            return int(float(total) - discount_price)
        return total
    class Meta:
        verbose_name_plural = 'orders'
    
class OrderItem(BaseModel):
    """
    Model for representing items in an order.

    This model stores information about items included in an order,
    such as the quantity and the product.

    Attributes:
        quantity (int): The quantity of the product in the order.
        order (ForeignKey): Reference to the order to which the item belongs.
        product (ForeignKey): Reference to the product included in the order.

    Methods:
        __str__():
            Returns a string representation of the order item.
        
        total_price():
            Calculates the total price of the order item.

    Meta:
        verbose_name_plural (str): Plural name for the model in the admin interface.
    """
    
    quantity = models.IntegerField()
    
    # Foreign Keys
    order = models.ForeignKey("Order", on_delete=models.CASCADE, related_name="order_items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="order_items")
    
    def __str__(self) -> str:
        return f"number of {self.product.name}: {self.quantity}"
    
    def total_price(self):
        return self.quantity * self.product.price
    class Meta:
        verbose_name_plural = 'order items'

class Cart(models.Model):
    """
    Model for representing a user's shopping cart.

    This model stores information about the items in a user's shopping cart,
    including the delivery details and the associated user.

    Attributes:
        province (str): The province for delivery.
        city (str): The city for delivery.
        detailed_address (str): Detailed address for delivery.
        postal_code (int): The postal code for delivery.
        created_at (DateTimeField): The date and time when the cart was created.
        updated_at (DateTimeField): The date and time when the cart was last updated.
        user (OneToOneField): Reference to the user who owns the cart.

    Methods:
        __str__():
            Returns a string representation of the cart.
        
        calculate_total_price():
            Calculates the total price of all items in the cart.

    Meta:
        verbose_name_plural (str): Plural name for the model in the admin interface.
    """
    
    province = models.CharField(max_length=255, blank=True, null=True, help_text="like Alborz")
    city = models.CharField(max_length=255, blank=True, null=True, help_text="like karaj")
    detailed_address = models.TextField(blank=True, null=True)
    postal_code = models.PositiveIntegerField(blank=True, null=True, help_text="like 3149757953")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    
    def __str__(self) -> str:
        return f"total cart: {self.calculate_total_price()}"
    
    def calculate_total_price(self):
        return sum(item.total_price() for item in self.cart_items.all())

    class Meta:
        verbose_name_plural = 'carts'

class CartItem(models.Model):
    """
    Model for representing an item in a shopping cart.

    This model stores information about the quantity of a product in a shopping cart.

    Attributes:
        quantity (int): The quantity of the product in the cart.
        created_at (DateTimeField): The date and time when the cart item was created.
        updated_at (DateTimeField): The date and time when the cart item was last updated.
        cart (ForeignKey): Reference to the cart to which the item belongs.
        product (ForeignKey): Reference to the product included in the cart item.

    Methods:
        __str__():
            Returns a string representation of the cart item.
        
        total_price():
            Calculates the total price of the cart item.

    Meta:
        verbose_name_plural (str): Plural name for the model in the admin interface.
    """
    
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Foreign Keys
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="cart_items")
    
    
    def __str__(self) -> str:
        return f"total price of {self.quantity} {self.product.name}: {self.total_price()}"
    
    def total_price(self):
        return self.quantity * self.product.price
    
    class Meta:
        verbose_name_plural = 'cart items'
        
class Coupon(BaseModel):
    """
    Model for representing coupons that users can apply to orders.

    This model stores information about coupons, including the code, percentage discount,
    expiration date, available quantity, usage limit per user, and activation status.

    Attributes:
        code (str): The unique code for the coupon.
        percentage (int): The percentage discount offered by the coupon.
        expiration_date (DateTimeField): The date and time when the coupon expires.
        available_quantity (int): The number of available uses for the coupon.
        usage_limit_per_user (int): The maximum number of times the coupon can be used per user.
        is_active (bool): Indicates whether the coupon is active.
        user (ManyToManyField): Reference to users who have this coupon.

    Methods:
        __str__():
            Returns a string representation of the coupon.

    Meta:
        verbose_name_plural (str): Plural name for the model in the admin interface.
    """
    
    code = models.CharField(max_length=30, unique=True, help_text="like DJke21x")
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    discount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(90)], db_column="discount")
    # max_discount = models.IntegerField()
    # available_quantity = models.PositiveIntegerField()
    # usage_limit_per_user = models.PositiveIntegerField()
    is_active = models.BooleanField(default=False)
    
    #Foreign Key
    user = models.ForeignKey(User, blank=True, on_delete=models.CASCADE, related_name="coupons") 
    
    def __str__(self) -> str:
        return f"{self.code} with {self.discount} percentage is active until {self.valid_to}."
    
    class Meta:
        verbose_name_plural = 'coupons'
        
class Transaction(BaseModel):
    """
    Model for representing transactions related to orders.

    This model stores information about transactions, including the final price,
    transaction type, and associated user and order.

    Attributes:
        TRANSACTION_TYPES (tuple): Choices for the type of transaction.
        final_price (DecimalField): The final price of the transaction.
        transaction_type (str): The type of transaction.
        user (ForeignKey): Reference to the user associated with the transaction.
        order (ForeignKey): Reference to the order associated with the transaction.

    Methods:
        __str__():
            Returns a string representation of the transaction.

    Meta:
        verbose_name_plural (str): Plural name for the model in the admin interface.
    """
    
    TRANSACTION_TYPES = (
    ("accounting transactions", "accounting transactions"),
    ("receipts", "receipts"),
)
    final_price = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=255, choices=TRANSACTION_TYPES) # deleted in ERD!
    
    # Foreign Keys
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="transacions")
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="transacions")
    
    def __str__(self) -> str:
        return f"transaction: {self.final_price}"
    
    class Meta:
        verbose_name_plural = "transactions"

