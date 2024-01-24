from django.db import models
from core.models import BaseModel
from accounts.models import User
from products.models import Product

# Create your models here.

class Order(BaseModel):
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=False)
    
    # Foreign keys
    user = models.ForeignKey("User", on_delete=models.PROTECT)
    discount_code = models.ForeignKey("DiscountCode", on_delete=models.PROTECT)
    
    
class OrderItem(BaseModel):
    quantity = models.IntegerField()
    
    # Foreign keys
    order = models.ForeignKey("Order", on_delete=models.PROTECT)
    product = models.ForeignKey("Product", on_delete=models.PROTECT)
    

class DiscountCode(BaseModel):
    code = models.CharField(max_length=255)
    percentage = models.IntegerField()
    expiration_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    
    # Foreign keys
    # user = models.ForeignKey("User", on_delete=models.PROTECT)
    
    
class Transaction(BaseModel):
    TRANSACTION_TYPES = (
    ("accounting transactions", "accounting transactions"),
    ("receipts", "receipts"),
)
    final_price = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    
    # Foreign Keys
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    order = models.OneToOneField(Order, on_delete=models.PROTECT,  primary_key=True)
    # discount_code = models.ForeignKey("DiscountCode", on_delete=models.PROTECT)
    
    