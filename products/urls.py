from django.urls import path
from . import views


app_name="products"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("category/<slug:category_slug>/", views.CategoryView.as_view(), name="category"),
    path("category/<slug:category_slug>/<slug:subcategory_slug>/products/", views.ProductView.as_view(), name="products"),
    path("products/<slug:slug>/", views.ProductDetailView.as_view(), name="product_detail"),

]


