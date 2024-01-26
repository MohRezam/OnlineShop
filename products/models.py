from django.db import models
from core.models import BaseModel
from accounts.models import User
from core.utils import category_image_path, product_image_path
# Create your models here.

class Category(BaseModel):
    name = models.CharField(max_length=255, unique=True)
    is_sub = models.BooleanField(default=False)
    image = models.ImageField(upload_to=category_image_path)
    
    # Foreign Keys
    parent_category = models.ForeignKey("self", on_delete=models.PROTECT)
    discount = models.ForeignKey("Discount", on_delete=models.PROTECT, null=True, blank=True)
    
    def __str__(self) -> str:
        return f"{self.name}"
    
    class Meta:
        verbose_name_plural = 'categories'
            
class Product(BaseModel):
    PRODUCT_ACTIVE_CHOICES = (
        (True, "Active"),
        (False, "Not Active"),
    )
    name = models.CharField(max_length=255)
    brand = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    slug = models.SlugField()
    features = models.ManyToManyField("ProductFeature", through='ProductFeatureValue')
    inventory_quantity = models.PositiveIntegerField()
    is_active = models.CharField(max_length=25, choices=PRODUCT_ACTIVE_CHOICES, default=True)
    image = models.ImageField(upload_to=product_image_path)
    
    
    # Foreign Keys
    user = models.ForeignKey(User, on_delete=models.PROTECT) # this relation is between staff and Product not customer.
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    discount = models.ForeignKey("Discount", on_delete=models.PROTECT, null=True, blank=True) # had blank and null True

    def __str__(self) -> str:
        return f"{self.name}"
    
    class Meta:
        verbose_name_plural = 'products'

class ProductFeature(BaseModel):
    name = models.CharField(max_length=255)
    text_value = models.TextField(blank=True, null=True)
    numeric_value = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    
    def __str__(self) -> str:
        return f"{self.name}"
    
    class Meta:
        verbose_name_plural = 'features'
class ProductFeatureValue(BaseModel):
    value = models.CharField(max_length=255)
    
    # Foreign Keys
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    feature = models.ForeignKey(ProductFeature, on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return f"{self.value} for {self.feature.name}"
    
    class Meta:
        verbose_name_plural = 'feature values'
class Comment(BaseModel):
    text = models.TextField()
    
    # Foreign Keys
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    products = models.ForeignKey("Product", on_delete=models.PROTECT)
    
    def __str__(self) -> str:
        return f"{self.text} by {self.user.first_name} {self.user.last_name}"

    class Meta:
        verbose_name_plural = 'comments'
        
class Discount(BaseModel):
    DISCOUNT_TYPE = (
        ("percentage", "Percentage"),
        ("decimal", "Decimal"),
    )
    type = models.CharField(max_length=255)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    max_value = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=False)
    
    # Foreign Keys
    user = models.ManyToManyField(User) # this relation is between staff and Discount not customer.
    
    def __str__(self) -> str:
        return f"{self.type}| {self.value}"
    
    class Meta:
        verbose_name_plural = 'discounts'
    
    
