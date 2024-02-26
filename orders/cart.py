
from decimal import Decimal
from django.conf import settings
from .serializers import ProductSerializer
from .models import Product
import json
from django.http import HttpResponse


# CART_SESSION_ID = 'cart'

# class Cart:
#     def __init__(self, request):
#         """
#         initialize the cart
#         """
#         self.session = request.session
#         cart = self.session.get(CART_SESSION_ID)
#         if not cart:
#             # save an empty cart in session
#             cart = self.session[CART_SESSION_ID] = {}
#         self.cart = cart

#     def save(self):
#         self.session.modified = True

#     def add(self, product, quantity=1, overide_quantity=False):
#         """
#         Add product to the cart or update its quantity
#         """

#         product_id = str(product.id)
#         if product_id not in self.cart:
#             self.cart[product_id] = {
#                 "quantity": 0,
#                 "price": str(product.price)
#             }
#         self.cart[product_id]["quantity"] += int(quantity)
#         self.save()

#     def remove(self, product):
#         """
#         Remove a product from the cart
#         """
#         product_id = str(product.id)

#         if product_id in self.cart:
#             del self.cart[product_id]
#             self.save()

#     def __iter__(self):
#         """
#         Loop through cart items and fetch the products from the database
#         """
#         product_ids = self.cart.keys()
#         products = Product.objects.filter(id__in=product_ids)
#         cart = self.cart.copy()
#         for product in products:
#             cart[str(product.id)]["product"] = ProductSerializer(product).data
#         for item in cart.values():
#             item["total_price"] = Decimal(item["price"]) * item["quantity"]
#             yield item

#     def __len__(self):
#         """
#         Count all items in the cart
#         """
#         return sum(item["quantity"] for item in self.cart.values())

#     def get_total_price(self):
#         return sum(Decimal(item["price"]) * item["quantity"] for item in self.cart.values())

#     def clear(self):
#         # remove cart from session
#         del self.session[CART_SESSION_ID]
#         self.save()
        

CART_COOKIE_NAME = "cart"

class Cart:
    def __init__(self, request):
        """
        initialize the cart
        """
        self.cookies = request.COOKIES
        
        cart_data = self.cookies.get(CART_COOKIE_NAME)
        if not cart_data:
            # If no cart data found in cookies, initialize an empty cart
            cart_data = "{}"
        
        self.cart = json.loads(cart_data)
    
    def save_cart_to_cookies(self, response):
        """
        Save the current cart data to cookies
        """
        cart_data = json.dumps(self.cart)
        response.set_cookie(key=CART_COOKIE_NAME, value=cart_data, max_age=604800)

    def add(self, product, quantity=1, overide_quantity=False):
        """
        Add product to the cart or update its quantity
        """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                "quantity": 0,
                "price": str(product.price)
            }
        self.cart[product_id]["quantity"] += int(quantity)

    def remove(self, product, response):
        """
        Remove a product from the cart
        """
        product_id = str(product.id)

        if product_id in self.cart:
            del self.cart[product_id]
            self.save_cart_to_cookies(response) 

    def __iter__(self):
        """
        Loop through cart items and fetch the products from the database
        """
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]["product"] = ProductSerializer(product).data
        for item in cart.values():
            item["total_price"] = Decimal(item["price"]) * item["quantity"]
            yield item
    # def __iter__(self):
    #     product_ids=self.cart.keys()
    #     products=Product.objects.filter(id__in=product_ids)
    #     cart=self.cart.copy()
    #     for product in products:
    #         cart[str(product.id)]['product']=product
    #     for item in cart.values():
    #         item['total_price']=int(item['price'])*item['quantity']
    #     yield item
    
    def __len__(self):
        """
        Count all items in the cart
        """
        return sum(item["quantity"] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item["price"]) * item["quantity"] for item in self.cart.values())

    def clear(self, response):
        self.cart = {}
        self.cookies['cart'] = {}
        self.save_cart_to_cookies(response)
        
