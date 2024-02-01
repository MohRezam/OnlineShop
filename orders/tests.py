from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Order, Coupon, OrderItem, CartItem, Cart, Transaction
from products.models import Product, Category
from django.utils import timezone



class OrderModelTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create(
            first_name='John',
            last_name='Doe',
            phone_number='09123456789',  
            email='john.doe@example.com',
            image="test/test/test",
            role='product manager',
            is_admin=False,
        )


        self.coupon = Coupon.objects.create(code='TESTCODE', percentage=1, expiration_date=timezone.now() + timezone.timedelta(days=7), available_quantity=100, usage_limit_per_user=3)

        self.order = Order.objects.create(
            total_price=100.00,
            is_paid=True,
            province='Test Province',
            city='Test City',
            detailed_address='Test Detailed Address',
            postal_code=12345,
            user=self.user,
            coupon=self.coupon,
        )

    def test_order_str_representation(self):
        expected_str = f"Total: {self.order.total_price}, Payment: {self.order.is_paid}"
        self.assertEqual(str(self.order), expected_str)

    def test_verbose_name_plural(self):
        self.assertEqual(Order._meta.verbose_name_plural, 'orders')

    def test_foreign_key_relationship_user(self):
        self.assertEqual(self.order.user, self.user)

    def test_foreign_key_relationship_coupon(self):
        self.assertEqual(self.order.coupon, self.coupon)



class OrderItemModelTest(TestCase):

    def setUp(self):
        self.product = Product.objects.create(name='Test Product',
                brand="Test Brand", 
                price=100, 
                description="Test Description", 
                slug="Test slug",
                inventory_quantity=100,
                user=get_user_model().objects.create_user(phone_number='09123456789', email='john.doe@example.com', first_name='John', last_name='Doe', password="123"),
                category=Category.objects.create(name="Test name"),
                )
        self.order = Order.objects.create(
            total_price=100.00,
            is_paid=True,
            province='Test Province',
            city='Test City',
            detailed_address='Test Detailed Address',
            postal_code=12345,
            user=get_user_model().objects.create_user(phone_number='09123456788', email='john.doe@example+.com', first_name='John', last_name='Doe', password="123"),
        )

        self.order_item = OrderItem.objects.create(
            quantity=2,
            order=self.order,
            product=self.product,
        )

    def test_order_item_str_representation(self):
        expected_str = f"number of {self.order_item.product.name}: {self.order_item.quantity}"
        self.assertEqual(str(self.order_item), expected_str)

    def test_verbose_name_plural(self):
        self.assertEqual(OrderItem._meta.verbose_name_plural, 'order items')

    def test_foreign_key_relationship_order(self):
        self.assertEqual(self.order_item.order, self.order)

    def test_foreign_key_relationship_product(self):
        self.assertEqual(self.order_item.product, self.product)




class CartModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(
            first_name='John',
            last_name='Doe',
            phone_number='09123456789',  
            email='john.doe@example.com',
            image="test/test/test",
            role='product manager',
            is_admin=False,
        )


        self.cart = Cart.objects.create(
            user=self.user,
            province='Test Province',
            city='Test City',
            detailed_address='Test Address',
            postal_code=12345
        )

    def test_cart_str_representation(self):
        self.assertEqual(str(self.cart), f"total cart: {self.cart.calculate_total_price()}")

    def test_calculate_total_price(self):
        cart_item = CartItem.objects.create(
            quantity=10,
            cart=self.cart,
            product = Product.objects.create(name='Test Product',
                brand="Test Brand", 
                price=100, 
                description="Test Description", 
                slug="Test slug",
                inventory_quantity=100,
                user=get_user_model().objects.create_user(phone_number='09123456788', email='john.doe@example3.com', first_name='John', last_name='Doe', password="123"),
                category=Category.objects.create(name="Test name"),
                )
        )

        expected_total_price = cart_item.total_price()

        self.assertEqual(self.cart.calculate_total_price(), expected_total_price)

    def test_verbose_name_plural(self):
        expected_verbose_name_plural = 'carts'
        self.assertEqual(Cart._meta.verbose_name_plural, expected_verbose_name_plural)
        


class CartItemModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(
            first_name='John',
            last_name='Doe',
            phone_number='09123456789',  
            email='john.doe@example.com',
            image="test/test/test",
            role='product manager',
            is_admin=False,
        )


        self.category = Category.objects.create(name="Test Category")

        self.product = Product.objects.create(
            name='Test Product',
            brand="Test Brand",
            price=100,
            description="Test Description",
            slug="test-slug",
            inventory_quantity=100,
            user=self.user,
            category=self.category,
        )

        self.cart = Cart.objects.create(
            user=self.user,
            province='Test Province',
            city='Test City',
            detailed_address='Test Address',
            postal_code=12345
        )

        self.cart_item = CartItem.objects.create(
            quantity=2,
            cart=self.cart,
            product=self.product,
            created_at=timezone.now(),
            updated_at=timezone.now(),
        )

    def test_cart_item_total_price(self):
        expected_total_price = self.cart_item.quantity * self.product.price
        self.assertEqual(self.cart_item.total_price(), expected_total_price)

    def test_cart_item_str_representation(self):
        expected_str = f"total price of {self.cart_item.quantity} {self.product.name}: {self.cart_item.total_price()}"
        self.assertEqual(str(self.cart_item), expected_str)
        
        

class CouponModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(
            first_name='John',
            last_name='Doe',
            phone_number='09123456789',  
            email='john.doe@example.com',
            image="test/test/test",
            role='product manager',
            is_admin=False,
        )


        self.coupon = Coupon.objects.create(
            code='TESTCODE',
            percentage=10,
            expiration_date=timezone.now() + timezone.timedelta(days=7),
            available_quantity=100,
            usage_limit_per_user=1,
            is_active=True,
        )
        self.coupon.user.add(self.user)

    def test_coupon_str_representation(self):
        expected_str = f"TESTCODE with 10 percentage is active until {self.coupon.expiration_date} for 100 people"
        self.assertEqual(str(self.coupon), expected_str)

    def test_coupon_user_relation(self):
        self.assertIn(self.user, self.coupon.user.all())

    def test_coupon_verbose_name_plural(self):
        self.assertEqual(str(Coupon._meta.verbose_name_plural), 'coupons')
        
        
 

class TransactionModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(
            first_name='John',
            last_name='Doe',
            phone_number='09123456789',  
            email='john.doe@example.com',
            image="test/test/test",
            role='product manager',
            is_admin=False,
        )


        self.order = Order.objects.create(
            total_price=100.00,
            is_paid=True,
            province='Test Province',
            city='Test City',
            detailed_address='Test Detailed Address',
            postal_code=12345,
            user=self.user
        )

        self.transaction = Transaction.objects.create(
            final_price=100.00,
            transaction_type='accounting transactions',
            user=self.user,
            order=self.order,
        )

    def test_transaction_str_representation(self):
        expected_str = f"transaction: {self.transaction.final_price}"
        self.assertEqual(str(self.transaction), expected_str)

    def test_transaction_user_foreign_key(self):
        self.assertEqual(self.transaction.user, self.user)

    def test_transaction_order_foreign_key(self):
        self.assertEqual(self.transaction.order, self.order)

    def test_transaction_verbose_name_plural(self):
        self.assertEqual(str(Transaction._meta.verbose_name_plural), 'transactions')