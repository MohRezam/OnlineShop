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

class CartView(View):   
    def get(self, request):
        return render(request, "orders/cart.html")
    
# with session
class CartAPI(APIView):
    def get(self, request, slug, format=None):
        cart = Cart(request)

        return Response(
            {"data": list(cart.__iter__()), 
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
        return Response(
            {"message": "cart updated"},
            status=status.HTTP_202_ACCEPTED)

# with cookies
# class CartAPI(APIView):
#     """
#     Single API to handle cart operations
#     """
#     def get(self, request, slug, format=None):
#         cart = Cart(request)

#         return JsonResponse(
#             {"data": list(cart), 
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
#         response = JsonResponse(
#             {"message": "cart updated"},
#             status=status.HTTP_202_ACCEPTED)
#         cart.save_cart_to_cookies(response)
#         return response
    
class CartRemoveView(View):
    def get(self, request, product_slug):
        cart = Cart(request)
        product = get_object_or_404(Product, slug=product_slug)
        cart.remove(product)        
        return redirect("orders:cart")
        
        
class OrderView(LoginRequiredMixin, View):
    def get(self, request):
        cart = Cart(request)
        order = Order.objects.create(user=request.user, total_price=cart.get_total_price())
        for item in cart:
            OrderItem.objects.create(order=order, product= item['product'], quantity=item['quantity'])
            cart.clear()
        return render(request, "orders/checkout.html")
    
class OrderAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, order_id):
        order = get_object_or_404(Order, pk=order_id)
        # coupon = Coupon(order=order)
        # coupon_ser = CouponSerializer(instance=coupon)
        order_ser = OrderSerializer(instance=order)
        
        responses_data = {
            # "coupon":coupon_ser.data,
            "order":order_ser.data,
            
        }
        return Response(data=responses_data, status=status.HTTP_200_OK)
    