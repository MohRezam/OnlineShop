from django.db import models
from core.models import BaseModel
from accounts.models import User
from core.utils import category_image_path, product_image_path, news_image_path
from django.utils.text import slugify
from django.urls import reverse
from django.core.exceptions import ValidationError
# Create your models here.

class Category(BaseModel):
    """
    Represents a product category.

    Attributes:
        name (str): The name of the category.
        slug (str): The slugified version of the category name, used for SEO-friendly URLs.
                    It must be unique within the database.
        is_sub (bool): A boolean field indicating whether the category is a subcategory.
        image (ImageField): The image associated with the category.
        parent_category (ForeignKey): A reference to the parent category if this category is a subcategory.
        discount (ForeignKey): A reference to the discount applied to products within this category.

    Methods:
        clean(): Custom validation method ensuring correct setup for subcategories and parent categories.
        validate_unique(): Custom validation method to ensure unique names for main categories.
        save(*args, **kwargs): Overrides the save method to set a default image and slug based on the category's properties.

    String Representation:
        __str__(): Returns a string representation of the category, showing the name and, if applicable, the parent category.

    Meta Options:
        verbose_name_plural (str): Specifies the plural name for the model in the admin interface.
    """
    
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
    """
    Represents a product available for sale.

    Attributes:
        name (str): The name of the product.
        brand (str): The brand of the product.
        price (Decimal): The price of the product.
        description (str): A description of the product.
        slug (str): The slugified version of the product name, used for SEO-friendly URLs.
        inventory_quantity (int): The quantity of the product available in stock.
        is_available (str): The availability status of the product, chosen from predefined choices.
        image (ImageField): The image associated with the product.
        user (ForeignKey): A reference to the user (staff) who added the product.
        category (ForeignKey): A reference to the category to which the product belongs.
        discount (ForeignKey): A reference to the discount applied to the product.

    Methods:
        save(*args, **kwargs): Overrides the save method to set a default image and slug based on the product's properties.

    String Representation:
        __str__(): Returns a string representation of the product, showing the category and name.

    Meta Options:
        verbose_name_plural (str): Specifies the plural name for the model in the admin interface.
        ordering (tuple): Specifies the default ordering for query sets of this model.
    """
    
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
    is_available = models.CharField(max_length=25, choices=PRODUCT_AVAILABLE_CHOICES, default="available")
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
    """
    Represents a feature that can be associated with products.

    Attributes:
        name (str): The name of the feature, e.g., "color".

    Methods:
        __str__(): Returns a string representation of the feature, showing its name.

    Meta Options:
        verbose_name_plural (str): Specifies the plural name for the model in the admin interface.
    """
    
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
    """
    Represents a specific value of a product feature associated with a product.

    Attributes:
        value (str): The value of the product feature, e.g., "red".

    Foreign Keys:
        product (ForeignKey): A reference to the product associated with this feature value.
        feature (ForeignKey): A reference to the product feature to which this value belongs.

    Methods:
        __str__(): Returns a string representation of the feature value, showing its value and associated feature name.

    Meta Options:
        verbose_name_plural (str): Specifies the plural name for the model in the admin interface.
    """
    
    value = models.CharField(max_length=255)
    
    # Foreign Keys
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="products_feature_value")
    feature = models.ForeignKey(ProductFeature, on_delete=models.CASCADE, related_name="products_feature_value")
    
    def __str__(self) -> str:
        return f"{self.value} for {self.feature.name}"
    
    class Meta:
        verbose_name_plural = 'feature values'
        
class Comment(BaseModel):
    """
    Represents a comment on a product.

    Attributes:
        text (str): The content of the comment.
        likes (int): The number of likes the comment has received.

    Foreign Keys:
        user (ForeignKey): A reference to the user who made the comment.
        product (ForeignKey): A reference to the product the comment is associated with.

    Methods:
        __str__(): Returns a string representation of the comment, showing its text and the name of the user who made it.

    Meta Options:
        verbose_name_plural (str): Specifies the plural name for the model in the admin interface.
    """
    
    text = models.TextField()
    likes = models.PositiveIntegerField(blank=True, null=True, default=0)
    
    # Foreign Keys
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    product = models.ForeignKey("Product", on_delete=models.CASCADE, related_name="comments", blank=True, null=True)
    
    def __str__(self) -> str:
        return f"{self.text} by {self.user.first_name} {self.user.last_name}"

    class Meta:
        verbose_name_plural = 'comments'
        
class Discount(BaseModel):
    """
    Represents a discount that can be applied to products.

    Attributes:
        type (str): The type of discount, e.g., "percentage" or "decimal".
        value (Decimal): The value of the discount.
        max_value (Decimal, optional): The maximum value the discount can have.
        expiration_date (datetime): The expiration date of the discount.
        is_active (bool): Indicates whether the discount is currently active.

    Foreign Keys:
        user (ManyToManyField): References to the users who can access this discount.

    Methods:
        __str__(): Returns a string representation of the discount, showing its type and value.

    Meta Options:
        verbose_name_plural (str): Specifies the plural name for the model in the admin interface.
    """
    
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
    """
    Represents a news article.

    Attributes:
        title (str): The title of the news article.
        body (str): The content of the news article.
        image (ImageField): An image associated with the news article.

    Foreign Keys:
        user (ForeignKey): A reference to the user who created the news article.

    Methods:
        __str__(): Returns a string representation of the news article, showing its title and creation date.

    Meta Options:
        verbose_name_plural (str): Specifies the plural name for the model in the admin interface.
    """
    
    title = models.CharField(max_length=255)
    body = models.TextField()
    image = models.ImageField(upload_to=news_image_path)
    
    # Foreign Keys
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="news")
    
    def __str__(self) -> str:
        return f"{self.title}-{self.created_at}"
    
    class Meta:
        verbose_name_plural = 'News'