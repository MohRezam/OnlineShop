from django.shortcuts import render, get_object_or_404
from django.views import View
from rest_framework.views import APIView
from .cart import Cart
from rest_framework.response import Response
from rest_framework import status
from products.models import Product
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Order, OrderItem, Coupon
from rest_framework.permissions import IsAuthenticated
from .serializers import OrderSerializer, ProductSerializer, CouponSerializer
from django.contrib import messages
from django.conf import settings
import requests
import json
from django.urls import reverse
import datetime
from accounts.serializers import AddressSerializer
from accounts.models import Address

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
    Single API to handle cart operations.

    This API handles operations related to a user's shopping cart, including
    retrieving the cart contents, adding or removing items, and clearing the cart.

    Methods:
        get(request, slug, format=None):
            Handles GET requests to retrieve the contents of the cart.

        post(request, slug, **kwargs):
            Handles POST requests to update the cart by adding, removing, or clearing items.

    Attributes:
        None
    """
    def get(self, request, slug, format=None):
        """
        Retrieves the contents of the cart.

        Args:
            request (HttpRequest): The HTTP request object.
            slug (str): The slug parameter used to identify the user.
            format (str, optional): The format of the response data. Defaults to None.

        Returns:
            JsonResponse: A JSON response containing the cart data and total price.

        Raises:
            None
        """
        
        cart = Cart(request)

        return JsonResponse(
            {"data": list(cart), 
            "cart_total_price": cart.get_total_price()},
            status=status.HTTP_200_OK
            )

    def post(self, request, slug,**kwargs):
        """
        Updates the cart by adding, removing, or clearing items.

        Args:
            request (HttpRequest): The HTTP request object.
            slug (str): The slug parameter used to identify the user.
            kwargs (dict): Additional keyword arguments.

        Returns:
            JsonResponse: A JSON response indicating the cart update status.

        Raises:
            None
        """
        
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
    """
    API view to remove a product from the cart.

    Methods:
        get(request, product_slug):
            Handles GET requests to remove a product from the cart.

    Attributes:
        None
    """
    
    def get(self, request, product_slug):
        """
        Removes a product from the cart.

        Args:
            request (HttpRequest): The HTTP request object.
            product_slug (str): The slug of the product to be removed.

        Returns:
            JsonResponse: A JSON response indicating the success of the operation.

        Raises:
            None
        """
        
        product = get_object_or_404(Product, slug=product_slug)
        cart = Cart(request)
        response = JsonResponse({'message': 'Product removed successfully'})
        cart.remove(product, response)
        messages.success(request, f"{product.name} removed successfully", "success")
        return response
        
   
class OrderDetailAPIView(APIView):
    """
    API view to retrieve and update order details.

    Methods:
        get(request, order_id):
            Handles GET requests to retrieve order details.

        post(request, order_id):
            Handles POST requests to update order details.

    Attributes:
        permission_classes (list): A list of permission classes to apply to the view.
    """
    
    permission_classes = [IsAuthenticated]
    def get(self, request, order_id):
        """
        Retrieves order details.

        Args:
            request (HttpRequest): The HTTP request object.
            order_id (int): The ID of the order to retrieve details for.

        Returns:
            Response: A JSON response containing order details, coupon data, and address data.

        Raises:
            None
        """
        
        order = get_object_or_404(Order, id=order_id)
        order_ser = OrderSerializer(instance=order)
        coupon = order.coupon
        coupon_ser = CouponSerializer(instance=coupon)
        addreses = Address.objects.filter(user=request.user)
        address_ser = AddressSerializer(instance=addreses, many=True)
        
        response_data = {
            "serializer":order_ser.data,
            "coupon_data":coupon_ser.data,
            "address_data":address_ser.data,
        }
        
        return Response(data=response_data, status=status.HTTP_200_OK)
    def post(self, request, order_id):
        """
        Updates order details.

        Args:
            request (HttpRequest): The HTTP request object.
            order_id (int): The ID of the order to update details for.

        Returns:
            Response: A JSON response containing updated order details and coupon data.

        Raises:
            None
        """
        
        now = datetime.datetime.now()
        coupon = CouponSerializer(data=request.data)
        if coupon.is_valid():
            code = coupon.validated_data["coupon_code"]
            try:
                coupon = Coupon.objects.get(code__exact=code, valid__from__lte=now, valid_to__gte=now, is_active=True)
            except Coupon.DoesNotExist:
                return Response({"message":"this coupon does not exists"})
            order = Order.objects.get(id=order_id)
            # order.discount = coupon.discount
            order.save()
            order_ser = OrderSerializer(order)
            coupon_ser = CouponSerializer(coupon)
        address = AddressSerializer(request.data)
        if address.is_valid():
            city = address.validated_data["city"]
            province = address.validated_data["province"]
            detail_address = address.validated_data["detail_address"]
            order = get_object_or_404(Order, id=order_id)
            order.province = province
            order.city = city
            order.detailed_address = detail_address
            order.save()
            
        response_data = {
            "serializer":order_ser.data,
            "coupon_data":coupon_ser.data,
        }
        return Response(data=response_data)
           
           
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
    
    
class OrderCreateView(APIView):
    permission_classes = [IsAuthenticated]
    
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
        response = Response(data=response_data, status=status.HTTP_200_OK)
        
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