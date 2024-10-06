import uuid
import random
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from products.models import Customer
from account.models import User
from utils.choices_utils import get_all_tier_choices
from utils.generator_utils import (
    mock_customer_generator,
    mock_user_generator,
    generate_phone_number,
)

TIER_CHOICES = get_all_tier_choices()


class CustomerDetailTest(APITestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = APIClient()
        cls.user = User.objects.create_user(**mock_user_generator())
        cls.client.force_authenticate(user=cls.user)
        cls.customer_data = mock_customer_generator()
        cls.customer = Customer.objects.create(**cls.customer_data)
        cls.url = reverse("customer_detail", kwargs={"id": cls.customer.id})

    def test_retrieve_existed_customer(self):
        response = self.client.get(self.url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.customer_data["name"])
        self.assertEqual(response.data["email"], self.customer_data["email"])
        self.assertEqual(response.data["phone"], self.customer_data["phone"])
        self.assertEqual(response.data["tier"], self.customer_data["tier"])
        self.assertEqual(response.data["fax"], self.customer_data["fax"])
        self.assertEqual(
            response.data["contact_list"], self.customer_data["contact_list"]
        )
        self.assertEqual(response.data["address"], self.customer_data["address"])
        self.assertEqual(response.data["note"], self.customer_data["note"])

    def test_retrieve_not_existed_customer(self):
        non_existent_id = uuid.uuid4()  # An ID that does not exist
        url = reverse("customer_detail", kwargs={"id": non_existent_id})
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_existed_customer(self):
        new_customer_data = mock_customer_generator()
        response = self.client.patch(self.url, new_customer_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], new_customer_data["name"])
        self.assertEqual(response.data["email"], new_customer_data["email"])
        self.assertEqual(response.data["phone"], new_customer_data["phone"])
        self.assertEqual(response.data["tier"], new_customer_data["tier"])
        self.assertEqual(response.data["fax"], new_customer_data["fax"])
        self.assertEqual(
            response.data["contact_list"], new_customer_data["contact_list"]
        )
        self.assertEqual(response.data["address"], new_customer_data["address"])
        self.assertEqual(response.data["note"], new_customer_data["note"])

    def test_update_not_existed_customer(self):
        non_existent_id = uuid.uuid4()
        url = reverse("customer_detail", kwargs={"id": non_existent_id})
        new_customer_data = mock_customer_generator()
        response = self.client.patch(url, new_customer_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_partial_update_customer(self):
        partial_data = {"phone": generate_phone_number()}
        response = self.client.patch(self.url, partial_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["phone"], partial_data["phone"])

    def test_delete_customer(self):
        response = self.client.delete(self.url, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Customer.objects.count(), 0)

    def test_delete_non_existed_customer(self):
        non_existent_id = uuid.uuid4()
        url = reverse("customer_detail", kwargs={"id": non_existent_id})
        response = self.client.delete(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_customer_with_invalid_data(self):
        invalid_data = {
            "email": "not-an-email",
        }
        response = self.client.patch(self.url, invalid_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class CustomerListCreateViewTest(APITestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = APIClient()
        cls.user = User.objects.create_user(**mock_user_generator())
        cls.client.force_authenticate(user=cls.user)
        cls.customers = [
            Customer.objects.create(**mock_customer_generator()) for _ in range(3)
        ]
        cls.customers_count = len(cls.customers)
        cls.url = reverse("customer_list_create")

    def add_bulk_customers(self, count):
        for _ in range(count):
            Customer.objects.create(**mock_customer_generator())

    def test_create_customer(self):
        test_customer = mock_customer_generator()
        response = self.client.post(self.url, test_customer, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Customer.objects.count(), 4)
        created_customer = Customer.objects.get(name=test_customer["name"])
        self.assertEqual(created_customer.name, response.data["name"])

    def test_create_customer_with_missing_fields(self):
        incomplete_data = {
            "name": "Test Customer",
            # Missing other required fields
        }
        response = self.client.post(self.url, incomplete_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_customer_with_duplicate_name(self):
        customer_data = mock_customer_generator()
        Customer.objects.create(**customer_data)
        response = self.client.post(self.url, customer_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_existed_customer(self):
        existing_customer = mock_customer_generator()
        existing_customer["name"] = self.customers[0].name
        response = self.client.post(self.url, existing_customer, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invalid_email(self):
        invalid_customer = mock_customer_generator()
        invalid_customer["email"] = "longnguyen@@gmail..com"
        response = self.client.post(self.url, invalid_customer, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invalid_phone_number(self):
        invalid_customer = mock_customer_generator()
        invalid_customer["phone"] = "0291049192"
        response = self.client.post(self.url, invalid_customer, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_customers(self):
        response = self.client.get(self.url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("count"), 3)
        customer_names = [customer["name"] for customer in response.data["results"]]
        expected_names = list(Customer.objects.values_list("name", flat=True))
        self.assertCountEqual(customer_names, expected_names)

    def test_filter_customers_by_tier(self):
        # Get a random tier from the database
        random_tier = random.choice(TIER_CHOICES)[0]

        response = self.client.get(self.url, {"tier": random_tier}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Get the count of customers with this tier from the database
        expected_count = Customer.objects.filter(tier=random_tier).count()
        self.assertEqual(len(response.data["results"]), expected_count)

        for customer in response.data["results"]:
            self.assertEqual(customer["tier"], random_tier)

    def test_search_customers_by_name(self):
        search_customer = self.customers[0]
        response = self.client.get(
            self.url, {"search": search_customer.name}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("count"), 1)
        self.assertEqual(response.data["results"][0]["name"], search_customer.name)

    def test_sort_customers_by_name_ascending(self):
        response = self.client.get(self.url, {"ordering": "name"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        sorted_names = sorted(
            [customer["name"] for customer in response.data["results"]]
        )
        response_names = [customer["name"] for customer in response.data["results"]]
        self.assertEqual(sorted_names, response_names)

    def test_sort_customers_by_name_descending(self):
        response = self.client.get(self.url, {"ordering": "-name"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        sorted_names = sorted(
            [customer["name"] for customer in response.data["results"]], reverse=True
        )
        response_names = [customer["name"] for customer in response.data["results"]]
        self.assertEqual(sorted_names, response_names)

    def test_pagination_first_page(self):
        additional_customers = random.randint(9, 17)
        self.add_bulk_customers(additional_customers)
        response = self.client.get(self.url, {"page": 1}, format="json")
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 10)
        self.assertIsNotNone(response.data["next"])

    def test_pagination_second_page(self):
        additional_customers = random.randint(9, 17)
        self.add_bulk_customers(additional_customers)
        response = self.client.get(self.url, {"page": 2}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(response.data["results"]),
            self.customers_count + additional_customers - 10,
        )
        self.assertIsNotNone(response.data["previous"])

    def test_pagination_with_page_size_param(self):
        response = self.client.get(self.url, {"page": 1, "page_size": 2}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)

    def test_pagination_beyond_available_pages(self):
        response = self.client.get(self.url, {"page": 999}, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_filter_and_search_customers(self):
        # Choose a random customer from the existing list
        specific_customer = random.choice(self.customers)
        specific_tier = specific_customer.tier
        specific_name = specific_customer.name

        # Perform the search and filter
        response = self.client.get(
            self.url, {"tier": specific_tier, "search": specific_name}, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("count"), 1)
        self.assertEqual(response.data["results"][0]["name"], specific_name)
        self.assertEqual(response.data["results"][0]["tier"], specific_tier)

        # Clean up
        specific_customer.delete()

    def test_empty_search_results(self):
        response = self.client.get(
            self.url, {"search": "NonExistentName"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("count"), 0)
        self.assertEqual(len(response.data["results"]), 0)

    def test_invalid_filter(self):
        response = self.client.get(self.url, {"tier": "invalid_tier"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("count"), 0)
        self.assertEqual(len(response.data["results"]), 0)
