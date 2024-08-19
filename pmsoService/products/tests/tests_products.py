from unicodedata import category
from utils.choices_utils import *
from http.client import responses
from unicodedata import category

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from products.models import Product
from account.models import User
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

def mock_product_generator():
	category = random.choice(CATEGORY_CHOICES)[1]
	return {
		"name": generate_random_string(category),
		"category": category,
		"quantity": random.randint(1, 10),
		"price": random.randint(1, 10)
	}

class TestProductsViews(APITestCase):

	@classmethod
	def setUpTestData(self):
		self.user = User.objects.create_user(username="user", password="test123")
		self.client = APIClient()
		self.urls_create = reverse("product_list_create")
		self.product = mock_product_generator()
		self.product_instance = Product.objects.create(**self.product)
		self.urls_detail = reverse("product_detail", kwargs={"id": self.product_instance.id})


	def test_create_product(self):
		self.client.force_authenticate(user=self.user)
		test_product = mock_product_generator()
		response = self.client.post( self.urls_create, test_product, format="json")
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)

	def test_create_existing_product(self):
		self.client.force_authenticate(user=self.user)
		response = self.client.post( self.urls_create, self.product, format="json")
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

	def test_list_product(self):
		self.client.force_authenticate(user=self.user)
		response = self.client.get(self.urls_create)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(len(response.data), 1)

	def test_create_invalid_product(self):
		self.client.force_authenticate(user=self.user)
		test_create_invalid_product_quantity = mock_product_generator()
		test_create_invalid_product_quantity.update(quantity = -10)
		response = self.client.post( self.urls_create, test_create_invalid_product_quantity, format="json")
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

	def test_get_existing_product(self):
		self.client.force_authenticate(user=self.user)
		response = self.client.get(self.urls_detail)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data["name"], self.product["name"])
		self.assertEqual(response.data["category"], self.product["category"])
		self.assertEqual(response.data["quantity"], self.product["quantity"])
		self.assertEqual(response.data["price"], self.product["price"])

	def test_get_non_existing_product(self):
		test_product_id = uuid.uuid4()
		response = self.client.get(reverse("product_detail", kwargs={"id": test_product_id}))
		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

	def test_update_non_existing_product(self):
		test_product_id = uuid.uuid4()
		test_new_product = mock_product_generator()
		response = self.client.patch(reverse("product_detail", kwargs={"id": test_product_id}), test_new_product, format="json")
		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

	def test_update_invalid_format_product(self):
		test_data_product_quantity = random.randint(-10, 0)
		response = self.client.patch(self.urls_detail, {"quantity": test_data_product_quantity}, format="json")
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

	def test_partial_update_existing_product(self):
		test_partial_invalid_product_quantity = random.randint(1, 10)
		response = self.client.patch(self.urls_detail, {"quantity": test_partial_invalid_product_quantity}, format="json")
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_delete_existing_product(self):
		response = self.client.delete(self.urls_detail, format = "json")
		self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

	def test_delete_non_existing_product(self):
		test_product_id = uuid.uuid4()
		response = self.client.delete(reverse("product_detail", kwargs={"id": test_product_id}), format = "json")
		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)