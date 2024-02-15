from django.contrib import admin
from .models import User, Address
from .forms import UserChangeForm, UserCreationForm
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

@admin.register(Address)   
class RegisterAdress(admin.ModelAdmin):
    list_display = ("province","city")

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
   
    list_display = ('email', 'phone_number','role','is_staff','first_name','last_name',)
    list_filter = ('is_staff',)
   
    fieldsets = (
        (None, {'fields': ('email', 'phone_number', 'first_name', 'last_name' ,'role' ,'password', 'image')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'last_login', 'groups', 'user_permissions')}),
    )

    add_fieldsets = (
        (None, {'fields':('phone_number', 'email', 'first_name', 'last_name' ,'role','password1', 'password2')}),
    )
    search_fields = ('email', 'first_name')
    ordering = ('first_name',)
    filter_horizontal = ('groups','user_permissions')
   
    def str(self) -> str:
        return super().str()
   
# @admin.register(OtpCode)
# class OtpCodeAdmin(admin.ModelAdmin):
#     list_display = ("phone_number", "code", "create_at")