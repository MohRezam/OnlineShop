from rest_framework import serializers
from .models import Category, Comment, News

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"
        


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
        
        
class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = "__all__"