from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.core.validators import EmailValidator
from core.models import BaseModel
from .managers import UserManager
from django.core.validators import RegexValidator
import re
from core.utils import user_image_path

# Create your models here.
class User(AbstractBaseUser):
    ROLE_CHOICES = (
        ("Product Manager", "Product Manager"),
        ("Supervisor", "Supervisor"),
        ("Operator", "Operator"),
        ("Customer", "Customer"),
    )    
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=11, unique=True, validators=[RegexValidator(r'^\d{11}$', message='Enter a valid 11-digit phone number.')])
    email = models.EmailField(max_length=255, unique=True, validators=[EmailValidator(message='Enter a valid email address.')])
    image = models.ImageField(upload_to=user_image_path)
    role = models.CharField(max_length=255, choices=ROLE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(auto_now=True, editable=False)
    is_active = models.BooleanField(default=False)
    
    objects = UserManager()
    
    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ["email", "first_name", "last_name"]
         
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
        # Additional validation (e.g., ensuring the length or format of the phone number)
        # For example:
        if len(cleaned_phone_number) != 11:
            raise ValueError('Phone number should be 11 digits long.')

        return cleaned_phone_number  
    def save(self, *args, **kwargs):
        self.phone_number = self.clean_phone_number(self.phone_number)
        self.email = self.email
        super().save(*args, **kwargs)
    
    def delete(self):
        self.is_deleted = True
        self.save()
            
    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        return True
    
    def has_module_perms(self, app_label):
        return True
    
    @property
    def is_staff(self):
        return self.is_admin
    
class Address(BaseModel):
    province = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    detailed_address = models.TextField()
    postal_code = models.IntegerField()
    
    #Foreign Keys
    user = models.ForeignKey(User, on_delete=models.PROTECT)