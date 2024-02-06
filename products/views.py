from django.shortcuts import render
from rest_framework.views import APIView
from .models import Category, Comment, News, Product
from rest_framework.response import Response
from .serializers import CategorySerializer, CommentSerializer, NewsSerializer, ProductSerializer
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import NotFound
# Create your views here.


class HomeView(APIView):
    def get(self, request):
        categories = Category.objects.filter(is_sub=False)
        comments = Comment.objects.all().order_by('-likes')[:10]
        news = News.objects.all()
        
        ser_cat_data = CategorySerializer(instance=categories, many=True)
        ser_comm_data = CommentSerializer(instance=comments, many=True)
        ser_news_data = NewsSerializer(instance=news, many=True)
        
        response_data = {
            'categories': ser_cat_data.data,
            'comments': ser_comm_data.data,
            'news':ser_news_data.data,
        }

        return Response(data=response_data, status=status.HTTP_200_OK)
    
    
class CategoryView(APIView):
    def get(self, request, category_slug):
        category = get_object_or_404(Category, slug=category_slug)
        subcategories = Category.objects.filter(parent_category=category)
        serializer = CategorySerializer(instance=subcategories, many=True)
        
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
    
class ProductView(APIView):
    def get(self, request, category_slug, subcategory_slug):
        category = get_object_or_404(Category, slug=category_slug)
        subcategory = get_object_or_404(Category, slug=subcategory_slug, parent_category=category)
        products = Product.objects.filter(category=subcategory)
        serializer = ProductSerializer(instance=products, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductDetailView(APIView):
    def get(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        serializer = ProductSerializer(instance=product)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
