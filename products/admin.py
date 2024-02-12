from django.contrib import admin
from .models import Category, Product, Comment, Discount, ProductFeature, ProductFeatureValue, News

# Register your models here.



@admin.register(ProductFeatureValue)
class ProductFeatureValueAdmin(admin.ModelAdmin):
    list_display = ("product", "feature", "value")
    search_fields = ("value", )
    list_filter = ("value", )
    ordering = ("value", )



@admin.register(ProductFeature)
class ProductFeatureAdmin(admin.ModelAdmin):
    list_display = ("name", )
    search_fields = ("name", )
    list_filter = ("name", )
    ordering = ("name", )




@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ("title", "body")
    search_fields = ("title", )
    list_filter = ("title", )
    ordering = ("title", )




@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'brand', 'price', 'is_available')
    search_fields = ("name", "brand", "price")
    list_filter = ("is_available", )
    
    
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "category":
            kwargs["queryset"] = db_field.related_model.objects.filter(is_sub=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_sub', 'parent_category')
    search_fields = ('name', 'is_sub')
    list_filter = ('is_sub', )
    
    
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