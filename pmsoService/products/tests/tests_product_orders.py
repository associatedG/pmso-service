from time import timezone

from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from datetime import datetime, timedelta
from http.client import responses

from utils.choices_utils import *
from products.models import *
from products.serializers import ProductOrderSerializer

import uuid
import string
import random

User = get_user_model()
CATEGORY_CHOICES = get_all_category_choices()
STATUS_CHOICES = get_all_status_choices()


def generate_random_string(length=10):
    """Generate a random string of a given length."""
    letters = string.ascii_letters + string.digits
    return "".join(random.choice(letters) for _ in range(length))


def mock_product_generator():
    """Generate mock user based on role"""
    return {
        "name": generate_random_string(),
        "category": random.choice(CATEGORY_CHOICES)[1],
        "quantity": random.randint(1, 10),
        "price": random.randint(1, 10),
    }


def mock_future_data_generator():
    now = timezone.now()
    days_in_future = now + timedelta(days=random.randint(6, 30))
    return days_in_future.strftime("%Y-%m-%d")


def mock_product_order_generator(staff_id, logistic_id, deliverer_id, products):
    status = random.choice(STATUS_CHOICES)[0]
    return {
        "is_urgent": random.choice([True, False]),
        "due_date": (timezone.now() + timedelta(days=random.randint(1, 5))).strftime(
            "%Y-%m-%d"
        ),
        "status": status,
        "sale_staff": staff_id,
        "logistic_staff": logistic_id,
        "deliverer": deliverer_id,
        "products": products,
    }


def mock_products_generator(product_ids):
    return [
        {"product_id": product_id, "quantity": random.randint(1, 10)}
        for product_id in product_ids
    ]


class TestProductOrderView(APITestCase):

    @classmethod
    def setUpTestData(self):
        self.user = User.objects.create_user(username="user", password="test123")
        self.staff = User.objects.create_user(username="staff", password="test123")
        self.logistic = User.objects.create_user(
            username="logistic", password="test123"
        )
        self.deliverer = User.objects.create_user(
            username="deliverer", password="test123"
        )
        self.urls_create = reverse("product_order_list_create")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def create_product_order(self, num_products):
        products = [
            Product.objects.create(**mock_product_generator())
            for _ in range(num_products)
        ]
        product_ids = [product.id for product in products]
        return mock_product_order_generator(
            self.staff.id,
            self.logistic.id,
            self.deliverer.id,
            mock_products_generator(product_ids),
        )

    def create_and_post_product_order(self, num_products):
        MOCK_PRODUCT_ORDER = self.create_product_order(num_products)

        response = self.client.post(self.urls_create, MOCK_PRODUCT_ORDER, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        return response

    def check_ordering(self, ordering_field):
        response = self.client.get(
            self.urls_create + f"?ordering={ordering_field}", format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        sorted_products_order = ProductOrder.objects.all().order_by(ordering_field)
        expected_data = ProductOrderSerializer(sorted_products_order, many=True).data

        response_date_sorted = sorted(
            response.data.get("results"), key=lambda value: value["id"]
        )
        expected_data_sorted = sorted(expected_data, key=lambda value: value["id"])

        self.assertEqual(response_date_sorted, expected_data_sorted)

    def create_multiple_product_orders(self, num_products=5, num_product_orders=10):
        for _ in range(num_product_orders):
            self.create_and_post_product_order(num_products)

    def test_create_product_order_with_single_product(self):
        num_products = 1
        response = self.create_and_post_product_order(num_products)

        product_order_id = response.data["id"]
        product_order = ProductOrder.objects.get(id=product_order_id)
        self.assertIsNotNone(product_order)

    def test_create_product_order_with_multiple_product(self):
        num_products = 2
        response = self.create_and_post_product_order(num_products)

        product_order_id = response.data["id"]
        product_order = ProductOrder.objects.get(id=product_order_id)
        self.assertIsNotNone(product_order)

    def test_update_quantity_product_order(self):
        num_products = 2
        response = self.create_and_post_product_order(num_products)

        product_order_id = response.data["id"]
        product_id = response.data["products"][0]["product"].get("id")
        initial_quantity = response.data["products"][0]["quantity"]

        new_quantity = initial_quantity + 1

        patch_url = reverse("product_order_detail", kwargs={"id": product_order_id})
        patch_data = {
            "products": [{"product_id": product_id, "quantity": new_quantity}]
        }
        response = self.client.patch(patch_url, patch_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_quantity = response.data["products"][0]["quantity"]
        self.assertEqual(updated_quantity, new_quantity)

    def test_get_product_order_with_single_product(self):
        num_products = 1
        response = self.create_and_post_product_order(num_products)

        product_order = response.data
        response = self.client.get(
            reverse("product_order_detail", kwargs={"id": product_order["id"]})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], str(product_order["id"]))
        self.assertEqual(response.data["status"], product_order["status"])

    def test_get_product_order_with_multiple_products(self):
        num_products = 2
        response = self.create_and_post_product_order(num_products)

        product_order = response.data
        response = self.client.get(
            reverse("product_order_detail", kwargs={"id": product_order["id"]})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], str(product_order["id"]))
        self.assertEqual(response.data["status"], product_order["status"])

    def test_filter_product_order_is_urgent(self):
        self.create_multiple_product_orders()

        response = self.client.get(self.urls_create + "?is_urgent=True", format="json")
        filtered_product_orders = ProductOrder.objects.all().filter(is_urgent=True)
        expected_data = ProductOrderSerializer(filtered_product_orders, many=True).data

        self.assertEqual(response.data.get("results"), expected_data)

    def test_filter_product_order_status(self):
        status = random.choice(STATUS_CHOICES)[0]
        self.create_multiple_product_orders()

        response = self.client.get(
            self.urls_create + f"?status={status}", format="json"
        )
        filtered_product_orders = ProductOrder.objects.all().filter(status=status)
        expected_data = ProductOrderSerializer(filtered_product_orders, many=True).data

        self.assertEqual(response.data.get("results"), expected_data)

    def test_filter_product_order_due_date(self):

        now = timezone.now().strftime("%Y-%m-%d")
        self.create_multiple_product_orders()

        response = self.client.get(
            self.urls_create
            + f"?due_date__gte={now}&due_date__={mock_future_data_generator()}",
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        filtered_product_orders = (
            ProductOrder.objects.all()
            .filter(due_date__gte=now)
            .filter(due_date__lte=mock_future_data_generator())
        )
        expected_data = ProductOrderSerializer(filtered_product_orders, many=True).data

        self.assertEqual(response.data.get("results"), expected_data)

    def test_sort_product_order_sort_urgent_ascending(self):
        self.create_multiple_product_orders()
        self.check_ordering("is_urgent")

    def test_sort_product_order_sort_urgent_descending(self):
        self.create_multiple_product_orders()
        self.check_ordering("-is_urgent")

    def test_sort_product_order_sort_due_date_ascending(self):
        self.create_multiple_product_orders()
        self.check_ordering("due_date")

    def test_sort_product_order_sort_due_date_descending(self):
        self.create_multiple_product_orders()
        self.check_ordering("-due_date")

    def test_sort_product_order_sort_created_at_ascending(self):
        self.create_multiple_product_orders()
        self.check_ordering("created_at")

    def test_sort_product_order_sort_created_at_descending(self):
        self.create_multiple_product_orders()
        self.check_ordering("-created_at")

    def test_pagination(self):
        num_products = 5
        num_product_orders = 12
        page_size = 10
        self.create_multiple_product_orders(num_products, num_product_orders)

        response = self.client.get(self.urls_create + f"?page=1", format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIsNotNone(response.data.get("next"))
        self.assertIsNone(response.data.get("previous"))

        product_orders_object = ProductOrder.objects.all()[:page_size]
        expected_data = ProductOrderSerializer(product_orders_object, many=True).data

        self.assertEqual(response.data.get("results"), expected_data)

    def test_get_non_existent_product_order(self):
        self.client.force_authenticate(user=self.user)
        non_existent_id = uuid.uuid4()
        response = self.client.get(
            reverse("product_order_detail", kwargs={"id": non_existent_id})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_product_order(self):
        num_products = random.randint(1, 5)
        product_order = self.create_and_post_product_order(num_products)
        product_order_id = product_order.data["id"]

        response = self.client.patch(
            reverse("product_order_detail", kwargs={"id": product_order_id}),
            {"status": "Giao Hàng"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "Giao Hàng")

    def test_delete_product_order(self):
        num_products = random.randint(1, 5)
        product_order = self.create_and_post_product_order(num_products)
        product_order_id = product_order.data["id"]

        response = self.client.delete(
            reverse("product_order_detail", kwargs={"id": product_order_id})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_cancel_product_order(self):
        num_products = random.randint(1, 5)
        product_order = self.create_and_post_product_order(num_products)
        product_order_id = product_order.data["id"]

        response = self.client.patch(
            reverse("product_order_detail", kwargs={"id": product_order_id}),
            {"status": "Mở"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "Mở")

    def test_cancel_already_canceled_product_order(self):
        num_products = random.randint(1, 5)
        product_order = self.create_and_post_product_order(num_products)
        product_order_id = product_order.data["id"]

        response = self.client.patch(
            reverse("product_order_detail", kwargs={"id": product_order_id}),
            {"status": "Mở"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
