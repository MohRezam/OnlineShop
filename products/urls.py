from django.urls import path
from . import views


app_name="products"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("category/<slug:category_slug>/", views.CategoryView.as_view(), name="category"),
    path("category/<slug:category_slug>/<slug:subcategory_slug>/products/", views.ProductView.as_view(), name="products"),
    path("products/<slug:product_slug>/", views.ProductDetailView.as_view(), name="product_detail"),
    path("about/", views.AboutUsView.as_view(), name="about"),
    path("contact/", views.ContactView.as_view(), name="contact"),

    
    path("api/", views.HomeAPIView.as_view(), name="home_api"),
    path("api/category/<slug:category_slug>/", views.CategoryAPIView.as_view(), name="category_api"),
    path("api/category/<slug:category_slug>/<slug:subcategory_slug>/products/", views.ProductAPIView.as_view(), name="products_api"),
    path("api/products/<slug:slug>/", views.ProductDetailAPIView.as_view(), name="product_detail_api"),
    path("api/searching/search/", views.ProductSearchAPIView.as_view(), name='product_search'),
]




