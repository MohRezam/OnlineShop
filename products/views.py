from django.shortcuts import render
from rest_framework.views import APIView
from .models import Category, Comment, News, Product, ProductFeature, ProductFeatureValue
from rest_framework.response import Response
from .serializers import (CategorySerializer,
CommentSerializer, NewsSerializer, ProductSerializer,
ProductFeatureSerializer, ProductFeatureValueSerializer, DiscountSerializer)
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import NotFound
from django .views import View
from rest_framework import filters 
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListAPIView
# Create your views here.


class HomeAPIView(APIView):
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
    
    
class CategoryAPIView(APIView):
    def get(self, request, category_slug):
        category = get_object_or_404(Category, slug=category_slug)
        subcategories = Category.objects.filter(parent_category=category)
        serializer = CategorySerializer(instance=subcategories, many=True)
        
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
    
class ProductAPIView(APIView, PageNumberPagination):
    page_size = 6
    filter_backends = [SearchFilter]
    search_fields = ['name', 'brand']
    def get(self, request, category_slug, subcategory_slug):
        category = get_object_or_404(Category, slug=category_slug)
        subcategory = get_object_or_404(Category, slug=subcategory_slug, parent_category=category)
        products = Product.objects.filter(category=subcategory, is_available="available")
        pagination_products = self.paginate_queryset(products, request, view=self)
        serializer = ProductSerializer(pagination_products, many=True)
        
        # serializer = ProductSerializer(products, many=True)
        
        
        return self.get_paginated_response(serializer.data)
        # return Response(data=serializer.data, status=status.HTTP_200_OK)

  

class ProductDetailAPIView(APIView):
    def get(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        serializer = ProductSerializer(instance=product)
        
        features = ProductFeature.objects.filter(products=product)
        features_serializer = ProductFeatureSerializer(instance=features, many=True)
        
        feature_values = ProductFeatureValue.objects.filter(product=product)
        feature_value_serializer = ProductFeatureValueSerializer(instance=feature_values, many=True)
        
        comments = Comment.objects.filter(product=product)
        comment_serializer = CommentSerializer(instance=comments, many=True)
        
        discount_serializer = DiscountSerializer(instance=product.discount)
        
        
        response_data = {
            "features":features_serializer.data,
            "feature_values":feature_value_serializer.data,
            "product":serializer.data,
            "discounts":discount_serializer.data,
            "comments":comment_serializer.data,
        }
        
        return Response(data=response_data, status=status.HTTP_200_OK)

class ProductSearchAPIView(ListAPIView, PageNumberPagination):
    queryset= Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [SearchFilter]
    search_fields = ["name", "brand"]
    page_size = 6
    
class HomeView(View):
    def get(self, request):
        return render(request, "products/index.html", {})
    


class CategoryView(View):
    def get(self, request, category_slug):
        return render(request, "products/subcategories.html", {})

class ProductView(View):
    def get(self, request, category_slug, subcategory_slug):
        return render(request, 'products/products.html', {})    

class ProductDetailView(View):
    def get(self, request, product_slug):
        return render(request, 'products/product_detail.html', {})


class AboutUsView(View):
    def get(self, request):
        return render(request, "products/about.html", {})
    
class ContactView(View):
    def get(self, request):
        return render(request, "products/contact.html", {})
    