"""Integration tests for Customer, Product, and ProductOrder models and APIs."""

from datetime import timedelta
import random
import string
import uuid
from django.utils import timezone
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model
from products.models import ProductOrder
from utils.choices_utils import get_all_category_choices, get_all_status_choices

User = get_user_model()
CATEGORY_CHOICES = get_all_category_choices()
STATUS_CHOICES = get_all_status_choices()

# Helper functions for generating mock data


def generate_random_string(length=10):
    """Generate a random string of a given length."""
    letters = string.ascii_letters + string.digits
    return "".join(random.choice(letters) for _ in range(length))


def mock_customer_generator():
    """Generate mock customer data"""
    contact_list = []
    for _ in range(1):
        contact = {
            "name": generate_random_string(6),
            "phone": f"0{random.choice('35789')}{random.randint(10000000, 99999999)}",
        }
        contact_list.append(contact)

    return {
        "name": f"Customer {generate_random_string(5)}",
        "phone": f"0{random.choice('35789')}{random.randint(10000000, 99999999)}",
        "email": f"{generate_random_string(8)}@example.com",
        "tier": random.choice(["tier 1", "tier 2", "tier 3"]),
        "fax": random.randint(100000, 999999),
        "contact_list": contact_list,
        "address": f"{random.randint(1, 100)} {generate_random_string(8)} Street",
        "note": f"Note {generate_random_string(20)}",
    }


def mock_product_generator():
    """Generate mock product data"""
    return {
        "name": f"Product {generate_random_string(5)}",
        "category": random.choice(CATEGORY_CHOICES)[1],
        "quantity": random.randint(1, 100),
        "price": random.randint(10, 1000),
    }


def mock_product_order_generator(customer_id, staff_id, product_ids):
    """Generate mock product order data"""
    products = []
    for product_id in product_ids:
        product = {"product_id": product_id, "quantity": random.randint(1, 10)}
        products.append(product)

    return {
        "is_urgent": random.choice([True, False]),
        "due_date": (timezone.now() + timedelta(days=random.randint(1, 30))).strftime(
            "%Y-%m-%d"
        ),
        "status": random.choice(
            [
                status
                for status in STATUS_CHOICES
                if status[0] not in ["Completed", "Cancelled"]
            ]
        )[0],
        "customer": customer_id,
        "sale_staff": staff_id,
        "logistic_staff": staff_id,
        "deliverer": staff_id,
        "products": products,
    }


class TestCustomerProductOrderIntegration(APITestCase):
    @classmethod
    def setUpTestData(cls):
        """Set up test data for the entire test case"""
        cls.user = User.objects.create_user(username="testuser", password="testpass")
        cls.client = APIClient()
        cls.client.force_authenticate(user=cls.user)
        cls.customer_url = reverse("customer_list_create")
        cls.product_url = reverse("product_list_create")
        cls.product_order_url = reverse("product_order_list_create")

    def bulk_create_instances(self, num_customers=5, num_products=10, num_orders=20):
        """Create multiple customers, products, and orders for testing"""
        customers = [self.create_customer() for _ in range(num_customers)]
        products = [self.create_products(1)[0] for _ in range(max(3, num_products))]

        for _ in range(num_orders):
            customer = random.choice(customers)
            product_subset = random.sample(products, k=random.randint(1, 3))
            product_ids = [product["id"] for product in product_subset]
            self.create_order(customer, product_ids)

        return customers, products

    def create_customer(self):
        """Create a single customer via API"""
        response = self.client.post(
            self.customer_url, mock_customer_generator(), format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        return response.data["id"]

    def create_products(self, count=3):
        """Create a specified number of products via API"""
        products = []
        for _ in range(count):
            response = self.client.post(
                self.product_url, mock_product_generator(), format="json"
            )
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            products.append(response.data)
        return products

    def create_order(self, customer_id, product_ids):
        """Create a single order via API"""
        order_data = mock_product_order_generator(
            customer_id=customer_id, staff_id=self.user.id, product_ids=product_ids
        )
        response = self.client.post(self.product_order_url, order_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        return response.data

    def test_create_customer_and_product_order(self):
        """Test creating a customer and associated product order"""
        customer_id = self.create_customer()
        products = self.create_products()
        product_ids = [product["id"] for product in products]
        self.create_order(customer_id, product_ids)

        # Verify customer creation
        customer_response = self.client.get(
            reverse("customer_detail", kwargs={"id": customer_id})
        )
        self.assertEqual(customer_response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(customer_response.data["id"])

        # Verify order creation
        order_response = self.client.get(self.product_order_url)
        self.assertEqual(order_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(order_response.data["results"]), 1)

        created_order = order_response.data["results"][0]
        self.assertIsNotNone(created_order["id"])
        self.assertEqual(str(created_order["customer"]), customer_id)

        # Verify products in the order
        order_product_ids = [
            product_item["product"]["id"] for product_item in created_order["products"]
        ]
        self.assertTrue(all(pid in product_ids for pid in order_product_ids))
        self.assertTrue(1 <= len(order_product_ids) <= 3)

    def test_create_order_with_invalid_customer(self):
        """Test creating an order with an invalid customer ID"""
        product = self.create_products(1)[0]
        order_data = mock_product_order_generator(
            customer_id=uuid.uuid4(), staff_id=self.user.id, product_ids=[product["id"]]
        )
        response = self.client.post(self.product_order_url, order_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("customer", response.data)

    def test_multiple_orders_per_customer(self):
        """Test creating multiple orders for a single customer"""
        customer_id = self.create_customer()
        product_id = self.create_products(1)[0]["id"]

        for _ in range(5):
            self.create_order(customer_id, [product_id])

        response = self.client.get(
            reverse("customer_detail", kwargs={"id": customer_id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["number_of_orders"], 5)

    def test_customer_order_count(self):
        """Test the order count for a customer"""
        customers, _ = self.bulk_create_instances(
            num_customers=1, num_products=5, num_orders=3
        )
        response = self.client.get(
            reverse("customer_detail", kwargs={"id": customers[0]})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["number_of_orders"], 3)

    def test_customer_current_order_count(self):
        """Test the current (non-completed) order count for a customer"""
        customer_id = self.create_customer()
        product_id = self.create_products(1)[0]["id"]

        for _ in range(5):
            self.create_order(customer_id, [product_id])

        # Mark two orders as completed
        orders = ProductOrder.objects.filter(customer_id=customer_id)
        for order in orders[:2]:
            self.client.patch(
                reverse("product_order_detail", kwargs={"id": order.id}),
                {"status": "Completed"},
                format="json",
            )

        response = self.client.get(
            reverse("customer_detail", kwargs={"id": customer_id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["number_of_orders"], 5)
        self.assertEqual(response.data["number_of_current_orders"], 3)

    def test_order_product_order_by_customer_name(self):
        """Test ordering of product orders by customer name"""
        self.bulk_create_instances(num_customers=5, num_products=10, num_orders=20)

        def check_order(order_by, reverse=False):
            """Helper function to check ordering"""
            ordered_products = ProductOrder.objects.order_by(order_by)
            customer_names = list(
                ordered_products.values_list("customer__name", flat=True)
            )
            self.assertEqual(customer_names, sorted(customer_names, reverse=reverse))

        # Check ordering in database
        check_order("customer__name")
        check_order("-customer__name", reverse=True)

        # Check ordering via API
        for ordering in ["-customer__name", "customer__name"]:
            response = self.client.get(self.product_order_url, {"ordering": ordering})
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            results = response.data["results"]
            customer_names = [result["customer_name"] for result in results]
            self.assertEqual(
                customer_names, sorted(customer_names, reverse=ordering.startswith("-"))
            )

        # Additional checks for descending and ascending order
        response = self.client.get(
            self.product_order_url, {"ordering": "-customer__name"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data["results"]
        customer_names = [result["customer_name"] for result in results]
        self.assertEqual(customer_names, sorted(customer_names, reverse=True))

        response = self.client.get(
            self.product_order_url, {"ordering": "customer__name"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data["results"]
        customer_names = [result["customer_name"] for result in results]
        self.assertEqual(customer_names, sorted(customer_names))
