from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model
from utils.choices_utils import *

import uuid
import string
import random
from products.models import Product, ProductOrder, ProductOrderProduct

User = get_user_model()
STATUS_CHOICES = get_all_status_choices()


def generate_random_string(length=10):
    letters = string.ascii_letters + string.digits
    return "".join(random.choice(letters) for _ in range(length))

class TestProductOrderView(APITestCase):

    @classmethod
    def setUpTestData(self):
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.client = APIClient()
        self.product = Product.objects.create(
            name="Test Product",
            category=STATUS_CHOICES[0][0],
            quantity=100,
            price=500.0
        )
        self.product_order = ProductOrder.objects.create(
            is_urgent=False,
            due_date=timezone.now().date(),
            status="In Production",
            sale_staff_id=self.user.id,
        )

    def test_create_product_order(self):
        self.client.force_authenticate(user=self.user)
        product_id = self.product.id

        data = {
            "is_urgent": True,
            "due_date": timezone.now().date(),
            "status": "Open",
            "products": [{
                "product_id": product_id,
                "quantity": 100,
            }]
        }

        response = self.client.post(reverse("product_order_list_create"), data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.product_order.refresh_from_db()
        self.assertEqual(self.product_order.status, "In Production")

    def test_get_product_order(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse("product_order_detail", kwargs={"id": self.product_order.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], str(self.product_order.id))
        self.assertEqual(response.data['status'], self.product_order.status)

    def test_get_non_existent_product_order(self):
        self.client.force_authenticate(user=self.user)
        non_existent_id = uuid.uuid4()
        response = self.client.get(reverse("product_order_detail", kwargs={"id": non_existent_id}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_product_order(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(
            reverse("product_order_detail", kwargs={"id": self.product_order.id}),
            {"status": "Delivering"},
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_product_order(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(reverse("product_order_detail", kwargs={"id": self.product_order.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_cancel_product_order(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(reverse("product_order_detail", kwargs={"id": self.product_order.id}),
                                     {"status" : "Cancelled"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], "Cancelled")

    def test_cancel_already_canceled_product_order(self):
        self.client.force_authenticate(user=self.user)
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(reverse("product_order_detail", kwargs={"id": self.product_order.id}),
                                     {"status": "Cancelled"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], "Cancelled")
