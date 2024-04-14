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
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator

# Create your views here.

class HomeAPIView(APIView):
    """
    API view to retrieve data for the home page including categories, top comments, and news.
    """
    serializer_class = CategorySerializer
    def get(self, request):
        """
        Retrieve data for the home page.
        """
        
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
    """
    API view to retrieve subcategories of a specific category.
    """
    serializer_class = CategorySerializer
    def get(self, request, category_slug):
        """
        Retrieve subcategories of a specific category.
        """
        
        category = get_object_or_404(Category, slug=category_slug)
        subcategories = Category.objects.filter(parent_category=category)
        serializer = CategorySerializer(instance=subcategories, many=True)
        
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
    
class ProductAPIView(APIView, PageNumberPagination):
    """
    API view to retrieve products belonging to a specific category and subcategory.
    """
    serializer_class = ProductSerializer
    page_size = 6
    filter_backends = [SearchFilter]
    search_fields = ['name', 'brand']
    def get(self, request, category_slug, subcategory_slug):
        """
        Retrieve products belonging to a specific category and subcategory.
        """
        
        category = get_object_or_404(Category, slug=category_slug)
        subcategory = get_object_or_404(Category, slug=subcategory_slug, parent_category=category)
        products = Product.objects.filter(category=subcategory, is_available="available")
        pagination_products = self.paginate_queryset(products, request, view=self)
        serializer = ProductSerializer(pagination_products, many=True)
        
        # serializer = ProductSerializer(products, many=True)
        
        
        return self.get_paginated_response(serializer.data)
        # return Response(data=serializer.data, status=status.HTTP_200_OK)

  

class ProductDetailAPIView(APIView):
    """
    API view to retrieve detailed information about a specific product.
    """
    serializer_class = ProductSerializer
    def get(self, request, slug):
        """
        Retrieve detailed information about a specific product.
        """
        
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

class ProductSearchAPIView(APIView):
    """
    API view to search products based on a search query.
    """
    
    def get(self, request, *args, **kwargs):
        queryset = Product.objects.all()
        search_query = self.request.query_params.get('search', None)
        
        if search_query:
            queryset = queryset.filter(name__icontains=search_query) | queryset.filter(brand__icontains=search_query)
        
        paginator = PageNumberPagination()
        paginator.page_size = 6
        result_page = paginator.paginate_queryset(queryset, request)
        serializer = ProductSerializer(result_page, many=True)
        
        response_data = {
            'results': serializer.data
        }
        
        return Response(response_data, status=status.HTTP_200_OK)
@method_decorator(cache_page(60 * 30), name='dispatch')    
class HomeView(View):
    def get(self, request):
        return render(request, "products/index.html", {})
    

@method_decorator(cache_page(60 * 30), name='dispatch')
class CategoryView(View):
    def get(self, request, category_slug):
        return render(request, "products/subcategories.html", {})
    
@method_decorator(cache_page(60 * 30), name='dispatch')    
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
    

class CommentAPIView(APIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    def get(self, request, slug):
        try:
            product_parent = Product.objects.get(slug=slug)
            comments = Comment.objects.filter(product=product_parent)
            serializer = CommentSerializer(comments, many=True)
            return Response({'comment': serializer.data}, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
    def post(self, request, slug):
        data = request.data
        product = Product.objects.get(slug=slug)
        Comment.objects.create(text=data["text"], user=request.user, product=product)
        return Response(status=status.HTTP_200_OK)
    
        # comment = CommentSerializer(data=request.data)
        # product = Product.objects.get(slug=slug)
        # if comment.is_valid():
        #     Comment.objects.create(text=comment.validated_data["text"], user=request.user, product=product)
        #     return Response(status=status.HTTP_200_OK)
        # print(comment.errors)
        # return Response(status=status.HTTP_400_BAD_REQUEST)


class CommentView(View):
    def get(self, request, slug):
        return render(request, 'products/comment.html', context={})