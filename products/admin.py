from django.contrib import admin
from .models import Category, Product, Comment, Discount, ProductFeature, ProductFeatureValue

# Register your models here.

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Comment)
admin.site.register(Discount)
admin.site.register(ProductFeature)
admin.site.register(ProductFeatureValue)