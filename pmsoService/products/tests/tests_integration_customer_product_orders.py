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
from utils.generator_utils import (
    mock_customer_generator,
    mock_product_generator,
    mock_product_order_generator,
    mock_user_generator,
)

User = get_user_model()

# Helper functions for generating mock data


class TestCustomerProductOrderIntegration(APITestCase):
    @classmethod
    def setUpTestData(cls):
        """Set up test data for the entire test case"""
        cls.user = User.objects.create_user(mock_user_generator)
        cls.client = APIClient()
        cls.client.force_authenticate(user=cls.user)
        cls.customer_url = reverse("customer_list_create")
        cls.product_url = reverse("product_list_create")
        cls.product_order_url = reverse("product_order_list_create")

    def bulk_create_instances(self, num_customers=5, num_products=10, num_orders=20):
        """Create multiple customers, products, and orders for testing"""
        customers = self.create_customer(num_customers)
        products = self.create_products(num_products)

        for _ in range(num_orders):
            customer = random.sample(customers, k=1)
            product_subset = random.sample(products, k=random.randint(1, 3))
            product_ids = [product["id"] for product in product_subset]
            self.create_order(customer, product_ids)

        self.assertEqual(ProductOrder.objects.count(), num_orders)
        return customers, products

    def create_customer(self, num_customers=1):
        """Create a single customer via API"""
        customers = []
        for _ in range(num_customers):
            response = self.client.post(
                self.customer_url, mock_customer_generator(), format="json"
            )
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            customers.append(response.data["id"])
        return customers

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

    def create_order(self, customer_ids, product_ids):
        """Create a single order via API"""
        customer_id = customer_ids[random.randint(0, len(customer_ids) - 1)]
        # print(customer_ids)
        order_data = mock_product_order_generator(
            customer_id=customer_id, staff_id=self.user.id, product_ids=product_ids
        )
        response = self.client.post(self.product_order_url, order_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        return response.data

    def test_create_customer_and_product_order(self):
        """Test creating a customer and associated product order"""
        customer_ids = self.create_customer()
        customer_id = customer_ids[0]
        products = self.create_products()
        product_ids = [product["id"] for product in products]
        self.create_order(customer_ids, product_ids)

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
        self.assertEqual(str(created_order["customer"]["id"]), str(customer_id))

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

    def test_customer_order_count(self):
        """Test the order count for a customer"""
        customer_ids = self.create_customer()
        product_ids = [product["id"] for product in self.create_products(5)]

        orders = []
        for _ in range(5):
            order = self.create_order(customer_ids, product_ids)
            orders.append(order["id"])

        response = self.client.get(
            reverse("customer_detail", kwargs={"id": customer_ids[0]})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["number_of_orders"], 5)
        # Query the database directly to get the number of current orders
        current_orders_count = ProductOrder.objects.filter(
            customer_id=customer_ids[0],
            status__in=["Open", "Planning Production", "In Production", "Delivering"],
        ).count()

        # Compare the database query result with the API response
        self.assertEqual(
            response.data["number_of_current_orders"], current_orders_count
        )

    def test_order_product_order_by_customer_name(self):
        """Test ordering of product orders by customer name"""
        self.bulk_create_instances(num_customers=10, num_products=10, num_orders=20)

        def check_order(order_by, reverse=False):
            """Helper function to check ordering"""
            response = self.client.get(self.product_order_url, {"ordering": order_by})
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            # Query the database directly
            db_order_by = order_by.lstrip("-")
            db_orders = ProductOrder.objects.all().order_by(db_order_by)
            if reverse:
                db_orders = db_orders.reverse()
            db_customer_names = [order.customer.name for order in db_orders][:10]

            # Compare API results with database query
            api_customer_names = [
                result["customer"]["name"] for result in response.data["results"]
            ]
            self.assertEqual(
                [name.lower() for name in api_customer_names],
                [name.lower() for name in db_customer_names],
            )

        # Check ordering via API
        check_order("customer__name")
        check_order("-customer__name", reverse=True)
