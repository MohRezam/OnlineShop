from django.contrib import admin
from .models import Category, Product, Comment, Discount, ProductFeature, ProductFeatureValue, News

# Register your models here.

# admin.site.register(Category)
# admin.site.register(Product)
# admin.site.register(Comment)
# admin.site.register(Discount)
admin.site.register(ProductFeature)
admin.site.register(ProductFeatureValue)
admin.site.register(News)


class ProductAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "category":
            kwargs["queryset"] = db_field.related_model.objects.filter(is_sub=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(Product, ProductAdmin)

class CategoryAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "parent_category":
            kwargs["queryset"] = Category.objects.filter(is_sub=False)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(Category, CategoryAdmin)

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