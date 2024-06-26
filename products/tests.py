from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Category, Discount, Product, ProductFeature, ProductFeatureValue, News, Comment
from django.utils import timezone


class CommonTestSetup(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create(
            first_name='John',
            last_name='Doe',
            phone_number='09123456789',  
            email='john.doe@example.com',
            image="test/test/test",
            role='product manager',
            is_staff=False,
        )


        cls.discount = Discount.objects.create(
            type="percentage",
            value=10,
            expiration_date=timezone.now() + timezone.timedelta(days=30),
        )

        cls.category = Category.objects.create(
            name='TestCategory',
            slug="test-product1",
            image="test/test/test",
            discount=cls.discount,
        )

class CategoryModelTest(CommonTestSetup):

    def test_category_str_representation(self):
        expected_str = str(self.category.name)
        self.assertEqual(str(self.category), expected_str)

    def test_category_parent_category_foreign_key(self):
        self.assertIsNone(self.category.parent_category)

        sub_category = Category.objects.create(
            name='TestSubCategory',
            is_sub=True,
            slug="test-product2",
            image="test/test/test",
            parent_category=self.category,
        )

        self.assertEqual(sub_category.parent_category, self.category)

    def test_category_discount_foreign_key(self):
        self.assertEqual(self.category.discount, self.discount)

    def test_category_verbose_name_plural(self):
        self.assertEqual(str(Category._meta.verbose_name_plural), 'categories')
        



class ProductModelTest(CommonTestSetup):
    def setUp(self):
        self.product = Product.objects.create(
            name='TestProduct',
            brand='TestBrand',
            price=100.0,
            description='TestDescription',
            slug='test-product3',
            inventory_quantity=50,
            is_available=True,
            image="test/test/test",
            user=self.user,
            category=self.category,
            discount=self.discount,
        )

    def test_product_str_representation(self):
        expected_str = f"{self.category}-{self.product.name}"
        self.assertEqual(str(self.product), expected_str)

    def test_product_user_foreign_key(self):
        self.assertEqual(self.product.user, self.user)

    def test_product_category_foreign_key(self):
        self.assertEqual(self.product.category, self.category)

    def test_product_discount_foreign_key(self):
        self.assertEqual(self.product.discount, self.discount)

    def test_product_verbose_name_plural(self):
        self.assertEqual(str(Product._meta.verbose_name_plural), 'products')
        
        
        

class ProductFeatureModelTest(TestCase):
    def setUp(self):
        self.product_feature = ProductFeature.objects.create(
            name='TestFeature',
            # text_value='TestTextValue',
            # numeric_value=10.0,
        )

    def test_product_feature_str_representation(self):
        expected_str = str(self.product_feature.name)
        self.assertEqual(str(self.product_feature), expected_str)

    # def test_product_feature_text_value(self):
    #     self.assertEqual(self.product_feature.text_value, 'TestTextValue')

    # def test_product_feature_numeric_value(self):
    #     self.assertEqual(self.product_feature.numeric_value, 10.0)

    def test_product_feature_verbose_name_plural(self):
        self.assertEqual(str(ProductFeature._meta.verbose_name_plural), 'features')
        
        
    


class ProductFeatureValueModelTest(CommonTestSetup):
    def setUp(self):
        self.product_feature = ProductFeature.objects.create(name='Test Feature')
        self.product = Product.objects.create(
            name='Test Product',
            brand='Test Brand',
            price=100,
            description='Test Description',
            slug='test-product4',
            inventory_quantity=10,
            is_available=True,
            image="test/test/test",
            user=self.user,  
            category=self.category  
        )

    def test_product_feature_value_creation(self):
        product_feature_value = ProductFeatureValue.objects.create(
            value='Test Value',
            product=self.product,
            feature=self.product_feature
        )

        saved_product_feature_value = ProductFeatureValue.objects.get(pk=product_feature_value.pk)

        self.assertEqual(saved_product_feature_value.value, 'Test Value')
        self.assertEqual(saved_product_feature_value.product, self.product)
        self.assertEqual(saved_product_feature_value.feature, self.product_feature)
        
        


class DiscountModelTest(CommonTestSetup):
    def test_discount_creation(self):
        discount = Discount.objects.create(
            type='percentage',
            value=10.0,
            expiration_date='2024-02-29T12:00:00+00:00',
            is_active=True
        )
        discount.user.add(self.user)
        saved_discount = Discount.objects.get(pk=discount.pk)

        self.assertEqual(saved_discount.type, 'percentage')
        self.assertEqual(saved_discount.value, 10.0)
        self.assertEqual(saved_discount.expiration_date.isoformat(), '2024-02-29T12:00:00+00:00')
        self.assertTrue(saved_discount.is_active)
        self.assertIn(self.user, saved_discount.user.all())
        
   
class NewsModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(
            first_name='John',
            last_name='Doe',
            phone_number='09123456789',  
            email='john.doe@example.com',
            image="test/test/test",
            role='product manager',
            is_staff=False,
        )
        self.news = News.objects.create(
            title="Test Title",
            body="Test Body",
            image="test/test/test",
            user=self.user
        )
        
    def test_news_str_representation(self):
        expected_str = str(self.news.title) + "-" + str(self.news.created_at)
        self.assertEqual(str(self.news), expected_str)
        
    def test_news_verbose_name_plural(self):
        self.assertEqual(str(News._meta.verbose_name_plural), 'News')
        
        


class CommentModelTest(CommonTestSetup):
    def setUp(self):
        self.product = Product.objects.create(
            name='Test Product',
            brand='Test Brand',
            price=100,
            description='Test Description',
            slug='test-product5',
            inventory_quantity=10,
            is_available=True,
            image="test/test/test",
            user=self.user,  
            category=self.category  
        )
        self.comment = Comment.objects.create(
            text='Test Comment',
            user=self.user,
            product=self.product
        )
        
    def test_comment_verbose_name_plural(self):
        verbose_name_plural = self.comment._meta.verbose_name_plural

        self.assertEqual(verbose_name_plural, 'comments')