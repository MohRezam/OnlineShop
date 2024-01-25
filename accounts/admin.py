from django.contrib import admin
from .models import User, Address
from django.contrib.auth.models import Group

# Register your models here.

admin.site.register(User)
admin.site.register(Address)
admin.site.unregister(Group)