from django.db import models
from core.models import BaseModel
from accounts.models import User
from core.utils import category_image_path, product_image_path
# Create your models here.

class Category(BaseModel):
    name = models.CharField(max_length=255)
    is_sub = models.BooleanField(default=False)
    image = models.ImageField(upload_to=category_image_path)
    
    # Foreign Keys
    parent_category = models.ForeignKey("self", on_delete=models.PROTECT)
    discount = models.ForeignKey("Discount", on_delete=models.PROTECT, null=True, blank=True)
    
    
class Product(BaseModel):
    name = models.CharField(max_length=255)
    brand = models.CharField(max_length=255)
    price = models.CharField(max_length=100)
    description = models.TextField()
    inventory_quantity = models.PositiveIntegerField()
    image = models.ImageField(upload_to=product_image_path)
    
    # Foreign Keys
    user = models.ForeignKey("User", on_delete=models.PROTECT)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    discount = models.ForeignKey("Discount", on_delete=models.PROTECT, null=True, blank=True)

    
class Discount(BaseModel):
    type = models.CharField(max_length=255)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    max_value = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=False)
    
    # Foreign Keys
    user = models.ManyToManyField("User", on_delete=models.PROTECT)
    
    
    
