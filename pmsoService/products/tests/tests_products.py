import dataclasses
from unicodedata import category
from utils.choices_utils import *
from http.client import responses
from unicodedata import category

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from products.models import Product
from account.models import User
from products.serializers import ProductSerializer

import uuid
import string
import random

CATEGORY_CHOICES = get_all_category_choices()

#generate random name for Product
def generate_random_string(category, length = 10):
	if category == "Cơ Khí Ô Tô":
		category = "Bồn"
	letters = string.ascii_letters + string.digits
	random_string = "".join(random.choice(letters) for _ in range(length))
	return f"{category}-{random_string}"

def mock_product_generator(category = None):
	if category is None:
		category = random.choice(CATEGORY_CHOICES)[1]
	return {
		"name": generate_random_string(category),
		"is_active": random.choice([True, False]),
		"category": category,
		"quantity": random.randint(1, 10),
		"price": random.randint(1, 10)
	}

class TestProductsViews(APITestCase):

	@classmethod
	def setUpTestData(self):
		self.admin = User.objects.create_superuser(username="admin", password="admin")
		self.user = User.objects.create_user(username="user", password="test123")
		self.client = APIClient()
		self.client.force_authenticate(user=self.user)
		self.urls_create = reverse("product_list_create")
		self.product = mock_product_generator()
		self.product_instance = Product.objects.create(**self.product)
		self.urls_detail = reverse("product_detail", kwargs={"id": self.product_instance.id})

	def create_products(self, category, count):
		for _ in range(count):
			response = self.client.post(self.urls_create, mock_product_generator(category), format="json")
			self.assertEqual(response.status_code, status.HTTP_201_CREATED)

	def check_ordering(self, ordering_field):
		response = self.client.get(self.urls_create + f"?ordering={ordering_field}", format="json")
		self.assertEqual(response.status_code, status.HTTP_200_OK)

		sorted_products = Product.objects.all().order_by(ordering_field)
		expected_data = ProductSerializer(sorted_products, many=True).data
		self.assertEqual(response.data.get('results'), expected_data)

	def test_create_product(self):
		test_product = mock_product_generator()
		response = self.client.post( self.urls_create, test_product, format="json")
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)

	def test_create_existing_product(self):
		response = self.client.post( self.urls_create, self.product, format="json")
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

	def test_list_product(self):
		self.client.post(self.urls_create, mock_product_generator(), format="json")
		response = self.client.get(self.urls_create)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data.get('count'), 2)

	def test_create_invalid_product(self):
		invalid_product_quantity = mock_product_generator()
		invalid_product_quantity.update(quantity = -10)
		response = self.client.post( self.urls_create, invalid_product_quantity, format="json")
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

	def test_get_existing_product(self):
		response = self.client.get(self.urls_detail)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data["name"], self.product["name"])
		self.assertEqual(response.data["category"], self.product["category"])
		self.assertEqual(response.data["quantity"], self.product["quantity"])
		self.assertEqual(response.data["price"], self.product["price"])

	def test_get_non_existing_product(self):
		test_invalid_product_id = uuid.uuid4()
		response = self.client.get(reverse("product_detail", kwargs={"id": test_invalid_product_id}))
		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

	def test_update_non_existing_product(self):
		test_invalid_product_id = uuid.uuid4()
		new_product = mock_product_generator()
		response = self.client.patch(reverse("product_detail", kwargs={"id": test_invalid_product_id}), new_product, format="json")
		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

	def test_update_invalid_format_product(self):
		test_invalid_product_quantity = random.randint(-10, -1)
		response = self.client.patch(self.urls_detail, {"quantity": test_invalid_product_quantity}, format="json")
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

	def test_partial_update_existing_product(self):
		test_invalid_product_quantity = random.randint(1, 10)
		response = self.client.patch(self.urls_detail, {"quantity":
			                                                test_invalid_product_quantity}, format="json")
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_delete_existing_product(self):
		response = self.client.delete(self.urls_detail, format = "json")
		self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

	def test_delete_non_existing_product(self):
		test_invalid_product_id = uuid.uuid4()
		response = self.client.delete(reverse("product_detail", kwargs={"id": test_invalid_product_id}), format = "json")
		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

	def test_filter_category(self):
		test_category = self.product["category"]
		self.create_products(test_category, 3)

		response = self.client.get(self.urls_create + f"?category={test_category}", format="json")
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data.get('count'), 4)

	def test_invalid_filter_category(self):
		invalid_category = "invalid"
		response = self.client.get(self.urls_create + f"?category={invalid_category}", format="json")
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data['count'], 0)
		self.assertEqual(len(response.data['results']), 0)

	def test_filter_is_active(self):
		test_category = self.product["category"]
		test_is_active = True
		self.create_products(test_category, 4)
		response = self.client.get(self.urls_create +
		                           f"?category={test_category}&is_active={test_is_active}", format="json")

		self.assertEqual(response.status_code, status.HTTP_200_OK)

		filtered_products = Product.objects.all().filter(is_active=test_is_active)
		expected_data = ProductSerializer(filtered_products, many=True).data

		self.assertEqual(response.data.get('results'), expected_data)

	def test_sort_name_by_name_ascending(self):
		test_category = self.product["category"]
		self.create_products(test_category, 3)
		self.check_ordering("name")

	def test_sort_name_by_name_descending(self):
		test_category = self.product["category"]
		self.create_products(test_category, 3)
		self.check_ordering("-name")

	def test_sort_name_by_price_ascending(self):
		test_category = self.product["category"]
		self.create_products(test_category, 3)
		self.check_ordering("price")

	def test_sort_name_by_price_descending(self):
		test_category = self.product["category"]
		self.create_products(test_category, 3)
		self.check_ordering("-price")

	def test_sort_name_by_quantity_ascending(self):
		test_category = self.product["category"]
		self.create_products(test_category, 3)
		self.check_ordering("quantity")

	def test_sort_name_by_quantity_descending(self):
		test_category = self.product["category"]
		self.create_products(test_category, 3)
		self.check_ordering("-quantity")

	def test_sort_name_by_is_active_ascending(self):
		test_category = self.product["category"]
		self.create_products(test_category, 3)
		self.check_ordering("is_active")

	def test_sort_name_by_is_active_descending(self):
		test_category = self.product["category"]
		self.create_products(test_category, 3)
		self.check_ordering("-is_active")

	def test_pagination(self):
		test_category = self.product["category"]
		page_size = 10
		self.create_products(test_category, 11)

		response = self.client.get(self.urls_create + f"?page=1", format="json")
		self.assertEqual(response.status_code, status.HTTP_200_OK)

		self.assertIsNotNone(response.data.get('next'))
		self.assertIsNone(response.data.get('previous'))

		sorted_products = Product.objects.all()[:page_size]
		expected_data = ProductSerializer(sorted_products, many=True).data
		self.assertEqual(response.data.get('results'), expected_data)