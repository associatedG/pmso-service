from unicodedata import category

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from products.models import Product
from account.models import User
import uuid
import string
import random

#generate random name for Product
def generate_random_string(category, length = 10):
	if category == "Cơ Khí Ô Tô":
		category = "Bồn"
	letters = string.ascii_letters + string.digits
	random_string = "".join(random.choice(letters) for _ in range(length))
	return f"{category}-{random_string}"

def mock_product_generator():
	category = random.choice(["Phuy", "Thùng", "Cơ Khí Ô Tô"])
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
		self.urls = reverse("product_list_create")
		self.product = mock_product_generator()
		Product.objects.create(**self.product)

	def test_create_product(self):
		self.client.force_authenticate(user=self.user)
		test_product = mock_product_generator()
		response = self.client.post( self.urls, test_product, format="json")
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertEqual(Product.objects.count(), 2)

	def test_create_existing_product(self):
		self.client.force_authenticate(user=self.user)
		response = self.client.post( self.urls, self.product, format="json")
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)