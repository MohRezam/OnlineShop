from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.core.validators import EmailValidator
from core.models import BaseModel
from .managers import UserManager
from django.core.validators import RegexValidator
import re
from core.utils import user_image_path
from django.utils import timezone

# Create your models here.
class User(AbstractBaseUser):
    ROLE_CHOICES = (
        ("product manager", "Product Manager"),
        ("supervisor", "Supervisor"),
        ("operator", "Operator"),
        # ("customer", "Customer"),
    )    
    ADMIN_CHOICES = (
        (True, "Admin"),
        (False, "Not Admin")
    )
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=11, unique=True, validators=[RegexValidator(r'^\d{11}$', message='Enter a valid 11-digit phone number.')])
    email = models.EmailField(max_length=255, unique=True, validators=[EmailValidator(message='Enter a valid email address.')])
    image = models.ImageField(upload_to=user_image_path, blank=True, null=True)
    role = models.CharField(max_length=255, choices=ROLE_CHOICES, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, default=None, editable=False)
    is_active = models.BooleanField(default=True) # when get otp code with SMS or email, then set this to True.
    is_admin = models.CharField(max_length=25, choices=ADMIN_CHOICES, default=False)
    
    objects = UserManager()
    
    USERNAME_FIELD = "phone_number" # this field 'phone_number here!' must always be unique!!!
    REQUIRED_FIELDS = ["email", "first_name", "last_name"] # password is going to be asked by django automatiacaly & phone_number will too because its in USERNAME_FIELD.
  
         
    def convert_to_english_numbers(self, input_str):
        persian_to_english = {
            '۰': '0',
            '۱': '1',
            '۲': '2',
            '۳': '3',
            '۴': '4',
            '۵': '5',
            '۶': '6',
            '۷': '7',
            '۸': '8',
            '۹': '9',
        }

        persian_pattern = re.compile(r'[۰-۹]')

        english_number_str = persian_pattern.sub(lambda x: persian_to_english[x.group()], input_str)

        return english_number_str
    

    def clean_phone_number(self, phone_number):
        cleaned_phone_number = self.convert_to_english_numbers(phone_number)
        if len(cleaned_phone_number) != 11:
            raise ValueError('Phone number should be 11 digits long.')

        return cleaned_phone_number  
    def save(self, *args, **kwargs):
        if not self.image:
            self.image = 'path/to/default/image.jpg'
        self.phone_number = self.clean_phone_number(self.phone_number)
        self.email = self.email
        super().save(*args, **kwargs)
    
    def delete(self):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save()
            
    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"
    
    def has_perm(self, perm, obj=None):
        return True
    
    def has_module_perms(self, app_label):
        return True
    
    @property
    def is_staff(self):
        return self.is_admin
    
    class Meta:
        verbose_name_plural = 'Users'
    
class Address(BaseModel):
    province = models.CharField(max_length=255, help_text="like Alborz")
    city = models.CharField(max_length=255, help_text="like karaj")
    detailed_address = models.TextField()
    postal_code = models.PositiveIntegerField(help_text="like 3149757953")
    is_actual_person = models.BooleanField(default=True)
    receiver_name = models.CharField(max_length=255, blank=True, null=True)
    receiver_last_name = models.CharField(max_length=255, blank=True, null=True)
    receiver_phone_number = models.CharField(max_length=11, blank=True, null=True)
    
    #Foreign Keys
    user = models.ForeignKey(User, on_delete=models.PROTECT) # this relation is between both customers and staff with Address.
    
    def __str__(self) -> str:
        return f"{self.city} {self.province} {self.detailed_address[:10]}..."
    class Meta:
        verbose_name_plural = 'Addresses'