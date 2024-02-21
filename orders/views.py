from django.shortcuts import render, get_object_or_404
from django.views import View
from rest_framework.views import APIView
from .cart import Cart
from rest_framework.response import Response
from rest_framework import status
from products.models import Product
from django.shortcuts import redirect
from django.http import JsonResponse
from django.http import HttpResponse
# Create your views here.


class CartView(View):   
    def get(self, request):
        return render(request, "orders/cart.html")
    
# with session
class CartAPI(APIView):
    """
    Single API to handle cart operations
    """
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
        