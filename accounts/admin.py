from django.contrib import admin
from.models import User,Address
from .forms import UserChangeForm,UserCreationForm
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class User_display(admin.ModelAdmin):
    list_display = ("first_name","last_name","phone_number","email","role")
   
class RegisterAdress(admin.ModelAdmin):
    list_display = ("province","city")


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
   
    list_display = ('email', 'phone_number','role','is_staff','first_name','last_name',)
    list_filter = ('is_staff',)
   
    fieldsets = (
        (None, {'fields': ('email', 'phone_number', 'first_name', 'last_name' ,'role' ,'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff','last_login','groups','user_permissions')}),
    )

    add_fieldsets = (
        (None, {'fields':('phone_number', 'email', 'first_name', 'last_name' ,'role','password1', 'password2')}),
    )
    search_fields = ('email', 'first_name')
    ordering = ('first_name',)
    filter_horizontal = ('groups','user_permissions')
   
    def str(self) -> str:
        return super().str()
   
   
admin.site.register(User,UserAdmin)
admin.site.register(Address,RegisterAdress)
from .models import User, Address
from django.contrib.auth.models import Group

# Register your models here.

# admin.site.register(User)
# admin.site.register(Address)
admin.site.unregister(Group)