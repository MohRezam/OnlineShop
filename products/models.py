from django.db import models
from core.models import BaseModel
from accounts.models import User
from core.utils import category_image_path, product_image_path, news_image_path
from django.utils.text import slugify
from django.urls import reverse
from django.core.exceptions import ValidationError
# Create your models here.

class Category(BaseModel):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    is_sub = models.BooleanField(default=False)
    image = models.ImageField(upload_to=category_image_path, blank=True, null=True)
    
    # Foreign Keys
    parent_category = models.ForeignKey("self", on_delete=models.CASCADE, blank=True, null=True, related_name="categories")
    discount = models.ForeignKey("Discount", on_delete=models.CASCADE, null=True, blank=True, related_name="categories")
    
    
    def clean(self):
        if self.is_sub and not self.parent_category:
            raise ValidationError("Subcategories must have a parent category.")
        
        if not self.is_sub and self.parent_category:
            raise ValidationError("Main categories cannot have a parent category.You should set is_sub to True for that.")
    
    def validate_unique(self, exclude=None):
        super().validate_unique(exclude)
        if not self.is_sub:
            if self.__class__.objects.filter(name=self.name, is_sub=False).exclude(pk=self.pk).exists():
                raise ValidationError({'name': ['Category with this name already exists.']})
    
    def save(self, *args, **kwargs):
        if not self.image:
            self.image = 'notfound/notfoundimage.jpg'
        if not self.slug:
            if self.is_sub:
                self.slug = slugify(self.parent_category.name + "-" + self.name)
            else:
                self.slug = slugify(self.name)
        super().save(*args, **kwargs)
        
    
    def __str__(self) -> str:
        if self.parent_category:
            return f"{self.name}-{self.parent_category}" # to prevent showing None in admin panel.
        else:
            return self.name
    
    class Meta:
        verbose_name_plural = 'categories'
            
class Product(BaseModel):
    PRODUCT_AVAILABLE_CHOICES = (
        ("available", "Available"),
        ("not available", "Not Available"),
    )
    name = models.CharField(max_length=255)
    brand = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(blank=True)
    inventory_quantity = models.PositiveIntegerField()
    is_available = models.CharField(max_length=25, choices=PRODUCT_AVAILABLE_CHOICES, default=True)
    image = models.ImageField(upload_to=product_image_path, blank=True, null=True)
    
    
    # Foreign Keys
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="products") # this relation is between staff and Product not customer.
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    discount = models.ForeignKey("Discount", on_delete=models.CASCADE, null=True, blank=True, related_name="products") # had blank and null True

    
    def save(self, *args, **kwargs):
        if not self.image:
            self.image = 'notfound/notfoundimage.jpg'
        if not self.slug:
            self.slug = slugify(self.category.parent_category.name + "-" + self.name)
        super().save(*args, **kwargs)
    
    
    def __str__(self) -> str:
        return f"{self.category}-{self.name}"
    
    class Meta:
        verbose_name_plural = 'products'
        ordering = ('name', 'brand')

class ProductFeature(BaseModel):
    name = models.CharField(max_length=255, help_text="like color")
    
    # text_value = models.TextField(blank=True, null=True)
    # numeric_value = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    
    #Foreign Keys
    products = models.ManyToManyField("Product", through='ProductFeatureValue', blank=True)

    
    def __str__(self) -> str:
        return f"{self.name}"
    
    class Meta:
        verbose_name_plural = 'features'
        
class ProductFeatureValue(BaseModel):
    value = models.CharField(max_length=255)
    
    # Foreign Keys
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="products_feature_value")
    feature = models.ForeignKey(ProductFeature, on_delete=models.CASCADE, related_name="products_feature_value")
    
    def __str__(self) -> str:
        return f"{self.value} for {self.feature.name}"
    
    class Meta:
        verbose_name_plural = 'feature values'
        
class Comment(BaseModel):
    text = models.TextField()
    likes = models.PositiveIntegerField(default=0)
    
    # Foreign Keys
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    product = models.ForeignKey("Product", on_delete=models.CASCADE, related_name="comments")
    
    def __str__(self) -> str:
        return f"{self.text} by {self.user.first_name} {self.user.last_name}"

    class Meta:
        verbose_name_plural = 'comments'
        
class Discount(BaseModel):
    DISCOUNT_TYPE = (
        ("percentage", "Percentage"),
        ("decimal", "Decimal"),
    )
    type = models.CharField(max_length=255, choices=DISCOUNT_TYPE)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    max_value = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    expiration_date = models.DateTimeField()
    is_active = models.BooleanField(default=False)
    
    user = models.ManyToManyField(User) # this relation is between staff and Discount not customer.
    
    def __str__(self) -> str:
        return f"{self.type}: {self.value}"
    
    class Meta:
        verbose_name_plural = 'discounts'
    
    
class News(BaseModel):
    title = models.CharField(max_length=255)
    body = models.TextField()
    image = models.ImageField(upload_to=news_image_path)
    
    # Foreign Keys
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="news")
    
    def __str__(self) -> str:
        return f"{self.title}-{self.created_at}"
    
    class Meta:
        verbose_name_plural = 'News'