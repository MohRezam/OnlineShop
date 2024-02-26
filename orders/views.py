from django.shortcuts import render, get_object_or_404
from django.views import View
from rest_framework.views import APIView
from .cart import Cart
from rest_framework.response import Response
from rest_framework import status
from products.models import Product
from django.shortcuts import redirect
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Order, OrderItem, Coupon
from rest_framework.permissions import IsAuthenticated
from .serializers import OrderSerializer, ProductSerializer, CouponSerializer
from django.contrib import messages
from rest_framework.renderers import JSONRenderer
from rest_framework.serializers import ValidationError

class CartView(View):   
    def get(self, request):
        return render(request, "orders/cart.html")
    
# # with session
# class CartAPI(APIView):
#     def get(self, request, slug, format=None):
#         cart = Cart(request)

#         return Response(
#             {"data": list(cart.__iter__()), 
#             "cart_total_price": cart.get_total_price()},
#             status=status.HTTP_200_OK
#             )

#     def post(self, request, slug,**kwargs):
#         cart = Cart(request)

#         if "remove" in request.data:
#             product = request.data["product"]
#             cart.remove(product)

#         elif "clear" in request.data:
#             cart.clear()

#         else:
#             product = request.data
#             cart.add(
#                     product=get_object_or_404(Product, slug=product["product"]),
#                     quantity=product["quantity"],
#                 )
#         return Response(
#             {"message": "cart updated"},
#             status=status.HTTP_202_ACCEPTED)

# with cookies
class CartAPI(APIView):
    """
    Single API to handle cart operations
    """
    def get(self, request, slug, format=None):
        cart = Cart(request)

        return JsonResponse(
            {"data": list(cart), 
            "cart_total_price": cart.get_total_price()},
            status=status.HTTP_200_OK
            )

    def post(self, request, slug,**kwargs):
        cart = Cart(request)

        if "remove" in request.data:
            product = request.data["product"]
            cart.remove(product)

        elif "clear" in request.data:
            cart.clear()

        else:
            product = request.data
            cart.add(
                    product=get_object_or_404(Product, slug=product["product"]),
                    quantity=product["quantity"],
                )
        response = JsonResponse(
            {"message": "cart updated"},
            status=status.HTTP_202_ACCEPTED)
        cart.save_cart_to_cookies(response)
        return response
    
class CartRemoveView(APIView):
    def get(self, request, product_slug):
        product = get_object_or_404(Product, slug=product_slug)
        cart = Cart(request)
        response = JsonResponse({'message': 'Product removed successfully'})
        cart.remove(product, response)
        messages.success(request, f"{product.name} removed successfully", "success")
        return response
        
   
class OrderDetailView(LoginRequiredMixin, View):
    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        return render(request, "orders/checkout.html")
           
     
# class OrderCreateView(LoginRequiredMixin, View):
#     def get(self, request):
#         cart = Cart(request)
#         order = Order.objects.create(user=request.user)
        
#         for item in cart:
#             product = item['product'] 
#             product_serializer = ProductSerializer(data=product)
#             print(f"Serialized product data: {product}")
#             if product_serializer.is_valid():
#                 print("Product serializer is valid.")
#                 product_instance = product_serializer.save()
#                 OrderItem.objects.create(order=order, product=product_instance, quantity=item['quantity'])
#             else:
#                 print("Product serializer is NOT valid. Errors:", product_serializer.errors)
        
#         cart.clear() 
#         return redirect("orders:order_detail", order.id)
    
    
class OrderCreateView(LoginRequiredMixin, View):
    # permission_classes = [IsAuthenticated]
    
    def get(self, request):
        cart = Cart(request)
        order = Order.objects.create(user=request.user)
        for item in cart:
            product_id = item["product"]["id"]
            quantity = item["quantity"]
            product = Product.objects.get(id=product_id)
            OrderItem.objects.create(order=order, product= product, quantity=quantity)
        return render(request, 'orders/checkout.html')  
    
class OrderAPIView(APIView):
    # permission_classes = [IsAuthenticated]
    def get(self, request, order_id):
        order = get_object_or_404(Order, pk=order_id)
        # coupon = Coupon(order=order)
        # coupon_ser = CouponSerializer(instance=coupon)
        order_ser = OrderSerializer(order)
        
        responses_data = {
            # "coupon":coupon_ser.data,
            "order":order_ser.data,
            
        }
        return Response(data=responses_data, status=status.HTTP_200_OK)
    