import random
import string
import uuid
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from products.models import Customer
from account.models import User


def generate_random_string(length=10):
    return "".join(random.choices(string.ascii_letters + string.digits, k=length))


def generate_phone_number():
    first_digit = "0"
    second_digit = random.choice(["3", "5", "7", "8", "9"])
    remaining_digits = "".join(random.choices("0123456789", k=8))
    return first_digit + second_digit + remaining_digits


def generate_customer_data(**kwargs):
    default_data = {
        "name": generate_random_string(),
        "email": f"{generate_random_string()}@example.com",
        "phone": generate_phone_number(),
        "tier": "tier 2",
        "fax": random.randint(100000, 999999),
        "contact_list": [
            {
                "name": generate_random_string(),
                "phone": generate_phone_number(),
            }
        ],
        "address": f"{random.randint(1, 999)} Nguyen Chi Thanh",
        "note": "Test customer note",
    }
    default_data.update(kwargs)
    return default_data


class CustomerDetailTest(APITestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = APIClient()
        cls.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        cls.client.force_authenticate(user=cls.user)
        cls.customer_data = generate_customer_data()
        cls.customer = Customer.objects.create(**cls.customer_data)
        cls.url = reverse(
            "customer_detail_update_destroy", kwargs={"id": cls.customer.id}
        )

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
        url = reverse("customer_detail_update_destroy", kwargs={"id": non_existent_id})
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_existed_customer(self):
        new_customer_data = generate_customer_data()
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
        url = reverse("customer_detail_update_destroy", kwargs={"id": non_existent_id})
        new_customer_data = generate_customer_data()
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
        url = reverse("customer_detail_update_destroy", kwargs={"id": non_existent_id})
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
        cls.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        cls.client.force_authenticate(user=cls.user)
        cls.customer_data = generate_customer_data()
        cls.customer = Customer.objects.create(**cls.customer_data)
        cls.url = reverse("customer_list_create")

    def test_create_customer(self):
        test_customer = generate_customer_data()
        response = self.client.post(self.url, test_customer, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Customer.objects.count(), 2)
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
        customer_data = generate_customer_data()
        Customer.objects.create(**customer_data)
        response = self.client.post(self.url, customer_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_existed_customer(self):
        existing_customer = generate_customer_data(name=self.customer.name)
        response = self.client.post(self.url, existing_customer, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invalid_email(self):
        invalid_customer = generate_customer_data(email="longnguyen@@gmail..com")
        response = self.client.post(self.url, invalid_customer, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invalid_phone_number(self):
        invalid_customer = generate_customer_data(phone="0291049192")
        response = self.client.post(self.url, invalid_customer, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_customers(self):
        response = self.client.get(self.url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], self.customer.name)