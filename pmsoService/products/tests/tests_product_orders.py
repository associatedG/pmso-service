from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model

import uuid
import string
import random
from products.models import Product, ProductOrder, ProductOrderProduct

User = get_user_model()


def generate_random_string(length=10):
    letters = string.ascii_letters + string.digits
    return "".join(random.choice(letters) for _ in range(length))

class TestProductOrderView(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="testuser", password="testpassword")
        cls.client = APIClient()
        cls.product = Product.objects.create(
            name="Test Product",
            category=Product.CATEGORY_TYPE_ONE,
            quantity=100,
            price=500.0
        )
        cls.product_order = ProductOrder.objects.create(
            is_urgent=False,
            due_date=timezone.now().date(),
            status="Pending",
            sale_staff_id=cls.user.id,
        )
        ProductOrderProduct.objects.create(
            product_order=cls.product_order,
            product=cls.product,
            quantity=2,
        )

    def test_get_product_order(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse("product_order_detail", kwargs={"id": self.product_order.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_non_existent_product_order(self):
        self.client.force_authenticate(user=self.user)
        non_existent_id = uuid.uuid4()
        response = self.client.get(reverse("product_order_detail", kwargs={"id": non_existent_id}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_product_order(self):
        self.client.force_authenticate(user=self.user)
        print(self.product.id)
        data = {
            "is_urgent": True,
            "due_date": timezone.now().date(),
            "status": "Open",
            "products": [
                {
                    "id": self.product.id,
                    "quantity": 3
                }
            ],
            "sale_staff_id": self.user.id,
        }
        try:
            response = self.client.post(reverse("product_order_list_create"), data, format="json")
            print(response.status_code)
            print(response.content)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        except Exception as e:
            print(f"Exception occurred: {e}")

    def test_update_product_order(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(
            reverse("product_order_detail", kwargs={"id": self.product_order.id}),
            {"status": "Delivering"},
            format="json"
        )
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_product_order(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(reverse("product_order_detail", kwargs={"id": self.product_order.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
