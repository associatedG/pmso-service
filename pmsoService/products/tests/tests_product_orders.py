from http.client import responses

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from products.models import *
from django.contrib.auth import get_user_model
import uuid
import string
import random

User = get_user_model()


def generate_random_string(length=10):
    """Generate a random string of a given length."""
    letters = string.ascii_letters + string.digits
    return "".join(random.choice(letters) for _ in range(length))


def mock_product_generator():
    """Generate mock user based on role"""
    return {
        "name": generate_random_string(),
        "category": "Phuy",
        "quantity": random.randint(1, 10),
        "price": random.randint(1, 10)
    }


def mock_product_order_generator(staff_id, logistic_id, deliverer_id, products):
    """Generate mock user based on role"""
    return {
            "is_urgent": True,
            "due_date": "2024-08-11",
            "sale_staff": staff_id,
            "logistic_staff": logistic_id,
            "deliverer": deliverer_id,
            "products": products
        }

def mock_products_generator(product_ids):
    return [{"product_id": product_id, "quantity": random.randint(1, 10)} for product_id in product_ids]


class TestProductOrderView(APITestCase):

    @classmethod
    def setUpTestData(self):
        self.user = User.objects.create_user(username="user", password="test123")
        self.staff = User.objects.create_user(username="staff", password="test123")
        self.logistic = User.objects.create_user(username="logistic", password="test123")
        self.deliverer = User.objects.create_user(username="deliverer", password="test123")
        self.client = APIClient()

    def test_create_product_order_with_single_product(self):
        test_product_1 = Product.objects.create(**mock_product_generator())
        self.client.force_authenticate(user=self.user)
        product_ids = [test_product_1.id]
        
        MOCK_PRODUCT_ORDER = mock_product_order_generator(self.staff.id, 
                                                          self.logistic.id, 
                                                          self.deliverer.id, 
                                                          mock_products_generator(product_ids))

        response = self.client.post(
            reverse("product_order_list_create"), MOCK_PRODUCT_ORDER, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        product_order_id = response.data["id"]
        product_order = ProductOrder.objects.get(id=product_order_id)
        self.assertIsNotNone(product_order)

    def test_create_product_order_with_multiple_product(self):
        test_product_1 = Product.objects.create(**mock_product_generator())
        test_product_2 = Product.objects.create(**mock_product_generator())
        self.client.force_authenticate(user=self.user)
        
        product_ids = [test_product_1.id, test_product_2.id]
        MOCK_PRODUCT_ORDER = mock_product_order_generator(self.staff.id,
                                                          self.logistic.id,
                                                          self.deliverer.id,
                                                          mock_products_generator(product_ids))

        response = self.client.post(
            reverse("product_order_list_create"), MOCK_PRODUCT_ORDER, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # def test_get_product_order(self):
    #     test_product = Product.objects.create(**mock_product_generator())
    #     product_ids = [test_product.id]
    #     MOCK_PRODUCT_ORDER = mock_product_order_generator(self.staff.id,
    #                                                       self.logistic.id,
    #                                                       self.deliverer.id,
    #                                                       mock_products_generator(product_ids))
    #     product_order = ProductOrder.objects.create(**MOCK_PRODUCT_ORDER)
    #     self.client.force_authenticate(user=self.user)
    #     print(f"Product_oder_id: {self.product_order.id}")
    #     response = self.client.get(reverse("product_order_detail", kwargs={"id": self.product_order.id}))
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(response.data['id'], str(self.product_order.id))
    #     self.assertEqual(response.data['status'], self.product_order.status)
