from django.db import models
from core.models import BaseModel
from accounts.models import User
from products.models import Product

# Create your models here.

class Order(BaseModel):
    PAYMENT_CHOICES = (
        (True, "Paid"),
        (False, "Not Paid")
    )
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.CharField(max_length=25, choices=PAYMENT_CHOICES)
    
    # Foreign keys
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="orders")
    coupon = models.ForeignKey("Coupon", on_delete=models.PROTECT, blank=True, null=True, related_name="orders")
    
    
class OrderItem(BaseModel):
    quantity = models.IntegerField()
    
    # Foreign keys
    order = models.ForeignKey("Order", on_delete=models.PROTECT, related_name="order_items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name="order_items")
    

class Coupon(BaseModel):
    code = models.CharField(max_length=255, unique=True)
    percentage = models.PositiveIntegerField(default=1)
    expiration_date = models.DateTimeField()
    available_quantity = models.PositiveIntegerField()
    usage_limit_per_user = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)
    
    # Foreign Keys
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="coupons")
    
    
class Transaction(BaseModel):
    TRANSACTION_TYPES = (
    ("accounting transactions", "accounting transactions"),
    ("receipts", "receipts"),
)
    final_price = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=255, choices=TRANSACTION_TYPES) # deleted in ERD!
    
    # Foreign Keys
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name="transactions")
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name="transactions")
    

