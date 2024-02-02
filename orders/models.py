from django.db import models
from core.models import BaseModel
from accounts.models import User
from products.models import Product

# Create your models here.
# def create_order_from_cart(self, cart): # this cart is an object of Cart model
#     order = self.create(user=cart.user, total_price=cart.calculate_total_price())

#     for cart_item in cart.cart_items.all():
#         OrderItem.objects.create(order=order, product=cart_item.product, quantity=cart_item.quantity)

#     cart.delete()

#     return order

class Order(BaseModel):
    PAYMENT_CHOICES = (
        ("paid", "Paid"),
        ("not paid", "Not Paid"),
    )
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.CharField(max_length=25, choices=PAYMENT_CHOICES, default=False) # when we create order from cart we have to set is_paid to True
    province = models.CharField(max_length=255, blank=True, null=True, help_text="like Alborz") # if user dont fill this it is going to fill by user address model informations
    city = models.CharField(max_length=255, blank=True, null=True, help_text="like karaj")
    detailed_address = models.TextField(blank=True, null=True)
    postal_code = models.PositiveIntegerField(blank=True, null=True, help_text="like 3149757953")
    
    # Foreign Keys
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    coupon = models.ForeignKey("Coupon", on_delete=models.PROTECT, blank=True, null=True)
    
    def __str__(self) -> str:
        return f"Total: {self.total_price}, Payment: {self.is_paid}"
    class Meta:
        verbose_name_plural = 'orders'
    
class OrderItem(BaseModel):
    quantity = models.IntegerField()
    
    # Foreign Keys
    order = models.ForeignKey("Order", on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    
    def __str__(self) -> str:
        return f"number of {self.product.name}: {self.quantity}"
    class Meta:
        verbose_name_plural = 'order items'

class Cart(models.Model):
    province = models.CharField(max_length=255, blank=True, null=True, help_text="like Alborz")
    city = models.CharField(max_length=255, blank=True, null=True, help_text="like karaj")
    detailed_address = models.TextField(blank=True, null=True)
    postal_code = models.PositiveIntegerField(blank=True, null=True, help_text="like 3149757953")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Foreign Keys
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    
    def __str__(self) -> str:
        return f"total cart: {self.calculate_total_price()}"
    
    def calculate_total_price(self):
        return sum(item.total_price() for item in self.cart_items.all())

    class Meta:
        verbose_name_plural = 'carts'

class CartItem(models.Model):
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Foreign Keys
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    
    
    def __str__(self) -> str:
        return f"total price of {self.quantity} {self.product.name}: {self.total_price()}"
    
    def total_price(self):
        return self.quantity * self.product.price
    
    class Meta:
        verbose_name_plural = 'cart items'
        
class Coupon(BaseModel):
    code = models.CharField(max_length=100, unique=True, help_text="like DJke21x")
    percentage = models.PositiveIntegerField(default=1)
    expiration_date = models.DateTimeField()
    available_quantity = models.PositiveIntegerField()
    usage_limit_per_user = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)
    
    # Foreign Keys
    user = models.ManyToManyField(User, blank=True) # fekr shavad
    
    def __str__(self) -> str:
        return f"{self.code} with {self.percentage} percentage is active until {self.expiration_date} for {self.available_quantity} people"
    
    class Meta:
        verbose_name_plural = 'coupons'
        
class Transaction(BaseModel):
    TRANSACTION_TYPES = (
    ("accounting transactions", "accounting transactions"),
    ("receipts", "receipts"),
)
    final_price = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=255, choices=TRANSACTION_TYPES) # deleted in ERD!
    
    # Foreign Keys
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    
    def __str__(self) -> str:
        return f"transaction: {self.final_price}"
    
    class Meta:
        verbose_name_plural = "transactions"

