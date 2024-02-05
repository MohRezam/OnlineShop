from django.shortcuts import render
from rest_framework.views import APIView
from .models import Category, Comment, News
from rest_framework.response import Response
from .serializers import CategorySerializer, CommentSerializer, NewsSerializer
from rest_framework import status
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