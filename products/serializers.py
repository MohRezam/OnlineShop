from rest_framework import serializers
from .models import Category, Comment, News, Product, ProductFeature, ProductFeatureValue, Discount
from accounts.models import User

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["name", "slug", "is_sub", "image", "parent_category", "discount"]
        


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["name", "brand", "price", "description", "slug",
        "inventory_quantity", "is_available", "image",
        "user", "category", "discount"]

        

class ProductFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductFeature
        fields = ["name", "products"]
        

    
class ProductFeatureValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductFeatureValue
        fields = ["value", "product", "feature"]
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields ='__all__'
            
class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Comment
        fields = ["text", "likes", "user", "product", "created_at"]



class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = ["type", "value", "max_value", "expiration_date", "is_active", "user"]


        
class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = ["title", "body", "image", "user"]