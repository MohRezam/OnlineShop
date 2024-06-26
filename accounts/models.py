from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.core.validators import EmailValidator, RegexValidator
from core.models import BaseModel
from .managers import UserManager
import re
from core.utils import user_image_path
from django.utils import timezone
from django.contrib.auth.models import PermissionsMixin

# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model representing a user in the system.

    Attributes:
        first_name (str): The first name of the user.
        last_name (str): The last name of the user.
        phone_number (str): The phone number of the user.
        email (str): The email address of the user.
        image (str): The profile image of the user.
        role (str): The role of the user in the system. Choices are "product manager", "supervisor", "operator", "customer", or "admin".
        created_at (datetime): The date and time when the user was created.
        updated_at (datetime): The date and time when the user was last updated.
        is_deleted (bool): Indicates if the user is deleted.
        deleted_at (datetime): The date and time when the user was deleted.
        is_active (bool): Indicates if the user account is active.
        is_staff (bool): Indicates if the user is a staff member.

    Methods:
        convert_to_english_numbers(input_str): Converts Persian numbers in the input string to English numbers.
        clean_role(role): Cleans and sets the role of the user.
        clean_phone_number(phone_number): Cleans the phone number by converting Persian numbers to English.
        save(*args, **kwargs): Overrides the save method to handle additional functionality.
        __str__(): Returns the string representation of the user.
    """
    
    
    ROLE_CHOICES = (
        ("product manager", "Product Manager"),
        ("supervisor", "Supervisor"),
        ("operator", "Operator"),
        ("customer", "Customer"),
        ("admin", "Admin")
    )    
   
    # ADMIN_CHOICES = (
    #     ("Admin", "Admin"),
    #     ("Not Admin", "Not Admin")
    # )
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
    # is_admin = models.CharField(max_length=25, choices=ADMIN_CHOICES, default=False)
    is_staff = models.BooleanField(default=False)
    
    objects = UserManager()
    
    USERNAME_FIELD = "email" # this should always be a unique field in the model.
    REQUIRED_FIELDS = ["phone_number", "first_name", "last_name"] # password is going to be asked by django automatiacaly & phone_number will too because its in USERNAME_FIELD.
    
         
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
    
    def clean_role(self, role):
        if role == "admin":
            self.is_superuser = True
            self.is_staff = True
        if role is None or role == "customer":
            self.role = "customer"
            self.is_staff = False
            # self.is_active = False # if the customer sent correct otpcode it will be True.
        else:
            self.is_staff = True
        return self.role
    
    def clean_phone_number(self, phone_number):
        cleaned_phone_number = self.convert_to_english_numbers(phone_number)
        # if len(cleaned_phone_number) != 11: # don't need this already checked this in the phone number field with RegexValidator.
        #     raise ValueError('Phone number should be 11 digits long.')
        return cleaned_phone_number  
    
    def save(self, *args, **kwargs):
        if not self.image:
            self.image = 'notfound/notfoundimage.jpg'
        self.role = self.clean_role(self.role)
        self.phone_number = self.clean_phone_number(self.phone_number)
        self.email = self.email
        super().save(*args, **kwargs)
    
    # def delete(self): # user soft delete
    #     self.is_deleted = True
    #     self.deleted_at = timezone.now()
    #     self.save()
            
    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"
    
    # def has_perm(self, perm, obj=None):
    #     return True
    
    # def has_module_perms(self, app_label):
    #     return True
    # @property
    # def is_staff(self):
    #     return self.is_admin
    
    class Meta:
        verbose_name_plural = 'Users'
    
    
# class OtpCode(models.Model):
#     phone_number = models.CharField(max_length=11)
#     code = models.PositiveSmallIntegerField()
#     create_at = models.DateTimeField(auto_now=True)
    
#     def __str__(self) -> str:
#         return f"{self.phone_number}-{self.code}-{self.create_at}"
    
    
    
class Address(BaseModel):
    """
    Model representing a user's address.

    Attributes:
        province (str): The province of the address.
        city (str): The city of the address.
        detailed_address (str): The detailed address information.
        postal_code (int): The postal code of the address.
        is_actual_person (bool): Indicates if the address belongs to an actual person.
        receiver_name (str): The first name of the receiver.
        receiver_last_name (str): The last name of the receiver.
        receiver_phone_number (str): The phone number of the receiver.

    Foreign Keys:
        user (User): The user associated with this address.

    Methods:
        __str__(): Returns the string representation of the address.
    """
    
    province = models.CharField(max_length=255, help_text="like Alborz")
    city = models.CharField(max_length=255, help_text="like karaj")
    detailed_address = models.TextField()
    postal_code = models.PositiveIntegerField(help_text="like 3149757953")
    is_actual_person = models.BooleanField(default=True)
    receiver_name = models.CharField(max_length=255, blank=True, null=True)
    receiver_last_name = models.CharField(max_length=255, blank=True, null=True)
    receiver_phone_number = models.CharField(max_length=11, blank=True, null=True)
    
    #Foreign Keys
    user = models.ForeignKey(User, on_delete=models.CASCADE) # this relation is between customers with Address.
    
    def __str__(self) -> str:
        return f"{self.city} {self.province} {self.detailed_address[:10]}..."
    class Meta:
        verbose_name_plural = 'Addresses'