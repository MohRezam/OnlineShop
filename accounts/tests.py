from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from .models import User, Address
from core.utils import user_image_path
from django.utils import timezone

class UserModelTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create(
            first_name='John',
            last_name='Doe',
            phone_number='09123456789',  
            email='john.doe@example.com',
            role='product manager',
            is_admin=False,
        )

    def test_user_str_representation(self):
        expected_str = f"{self.user.first_name} {self.user.last_name}"
        self.assertEqual(str(self.user), expected_str)

    def test_clean_phone_number_valid(self):
        cleaned_phone_number = self.user.clean_phone_number('09123456789')
        self.assertEqual(cleaned_phone_number, '09123456789')

    def test_clean_phone_number_invalid_length(self):
        with self.assertRaises(ValueError):
            self.user.clean_phone_number('123')  # Phone number should be 11 digits long

    def test_save_method(self):
        self.user.phone_number = '۰۹۱۲۳۴۵۶۷۸۹'
        self.user.save()
        self.assertEqual(self.user.phone_number, '09123456789')
        self.assertEqual(self.user.email, 'john.doe@example.com')

    def test_delete_method(self):
        self.user.delete()
        self.assertTrue(self.user.is_deleted)
        self.assertIsNotNone(self.user.deleted_at)
        self.assertEqual(self.user.deleted_at.date(), timezone.now().date())



class AddressModelTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(phone_number='09123456789',
            email='john.doe@example.com',
            first_name='John',
            last_name='Doe',
            password="123")
        

        self.address = Address.objects.create(
            province='Test Province',
            city='Test City',
            detailed_address='Test Detailed Address',
            postal_code=12345,
            is_actual_person=True,
            receiver_name='Test Receiver Name',
            receiver_last_name='Test Receiver Last Name',
            receiver_phone_number='1234567890',
            user=self.user,
        )

    def test_address_str_representation(self):
        expected_str = f"{self.address.city} {self.address.province} {self.address.detailed_address[:10]}..."
        self.assertEqual(str(self.address), expected_str)

    def test_verbose_name_plural(self):
        self.assertEqual(Address._meta.verbose_name_plural, 'Addresses')

    def test_foreign_key_relationship(self):
        self.assertEqual(self.address.user, self.user)

