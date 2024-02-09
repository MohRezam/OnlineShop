from django.contrib import admin
from .models import Category, Product, Comment, Discount, ProductFeature, ProductFeatureValue, News

# Register your models here.

admin.site.register(ProductFeature)
admin.site.register(ProductFeatureValue)
admin.site.register(News)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "category":
            kwargs["queryset"] = db_field.related_model.objects.filter(is_sub=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "parent_category":
            kwargs["queryset"] = Category.objects.filter(is_sub=False)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'created_at', 'product') 
    search_fields = ('text', 'user', 'likes')  
    list_filter = ('product',)
    ordering = ('-likes',)
    
    
@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'value', 'expiration_date')  
    search_fields = ('user',)  
    list_filter = ('is_active',)  
    ordering = ('-expiration_date',)