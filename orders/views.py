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
from django.conf import settings
import requests
import json
from django.urls import reverse

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
        
   
class OrderDetailAPIView(APIView):
    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        serializer = OrderSerializer(order)
        return Response({'serializer':serializer.data})
           
           
class OrderDetailView(View):
    def get(self, request, order_id):
        return render(request, 'orders/checkout.html')
     
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
            OrderItem.objects.create(order=order, product=product, quantity=quantity)
        
        # Construct the JSON response
        response_data = {
            "message": "Cart cleared successfully",
            "redirect_url": reverse("orders:order_detail", kwargs={"order_id": order.id})  # Replace "some_url_name" with the name of the URL you want to redirect to
        }
        response = JsonResponse(response_data)
        
        # Clear the cart
        cart.clear(response)
        
        return response
    
# class OrderAPIView(APIView):
#     # permission_classes = [IsAuthenticated]
#     def get(self, request, order_id):
#         order = get_object_or_404(Order, pk=order_id)
#         # coupon = Coupon(order=order)
#         # coupon_ser = CouponSerializer(instance=coupon)
#         order_ser = OrderSerializer(order)
        
#         responses_data = {
#             # "coupon":coupon_ser.data,
#             "order":order_ser.data,
            
#         }
#         return Response(data=responses_data, status=status.HTTP_200_OK)
    
    
if settings.SANDBOX:
    sandbox = 'sandbox'
else:
    sandbox = 'www'


ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
ZP_API_VERIFY = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"
description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required
CallbackURL = 'http://127.0.0.1:8080/orders/verify/'

class OrderPayView(LoginRequiredMixin, View):
    def get(self, request, order_id):
        order = Order.objects.get(id=order_id)
        request.session['order_pay'] = {
            'order_id': order.id,
        }
        data = {
            "MerchantID": settings.MERCHANT,
            "Amount": str(order.calculate_total_price()),  # Convert Decimal to string
            "Description": description,
            "Phone": request.user.phone_number,
            "CallbackURL": CallbackURL,
        }
        data = json.dumps(data)
        # set content length by data
        headers = {'content-type': 'application/json', 'content-length': str(len(data))}
        try:
            response = requests.post(ZP_API_REQUEST, data=data, headers=headers, timeout=10)

            if response.status_code == 200:
                response_data = response.json()
                if response_data['Status'] == 100:
                    return JsonResponse({'status': True, 'url': ZP_API_STARTPAY + str(response_data['Authority']), 'authority': response_data['Authority']})
                else:
                    return JsonResponse({'status': False, 'code': str(response_data['Status'])})
            return JsonResponse(response_data)

        except requests.exceptions.Timeout:
            return JsonResponse({'status': False, 'code': 'timeout'})
        except requests.exceptions.ConnectionError:
            return JsonResponse({'status': False, 'code': 'connection error'})


class OrderVerifyView(LoginRequiredMixin, View):
    def get(self, request):
        order_id = request.session["order_pay"]["order_id"]
        order = Order.objects.get(id=int(order_id))
        data = {
        "MerchantID": settings.MERCHANT,
        "Amount": order.calculate_total_price(),
        "Authority": request.GET['Authority'],
    }
        data = json.dumps(data)
        # set content length by data
        headers = {'content-type': 'application/json', 'content-length': str(len(data)) }
        response = requests.post(ZP_API_VERIFY, data=data,headers=headers)

        if response.status_code == 200:
            order.is_paid = True
            order.save()
            response = response.json()
            if response['Status'] == 100:
                return {'status': True, 'RefID': response['RefID']}
            else:
                return {'status': False, 'code': str(response['Status'])}
        return response