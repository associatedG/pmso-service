import random
import string
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from products.models import Customer
from account.models import User


def generate_random_string(length=10):
    return "".join(random.choices(string.ascii_letters + string.digits, k=length))


def generate_customer_data(
    name=None,
    email=None,
    phone=None,
    tier=None,
    fax=None,
    contact_list=None,
    address=None,
    note=None,
):
    return {
        "name": name or generate_random_string(),
        "email": email or f"{generate_random_string()}@example.com",
        "phone": phone or f"+84 {random.randint(100000000, 999999999)}",
        "tier": tier or "T2",
        "fax": fax or random.randint(100000, 999999),
        "contact_list": contact_list
        or [
            {
                "name": generate_random_string(),
                "phone": f"+84{random.randint(100000000, 999999999)}",
            }
        ],
        "address": address or f"{random.randint(1, 999)} Nguyen Chi Thanh",
        "note": note or "Test customer note",
    }


class CustomerListCreateViewTest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        cls.client = APIClient()
        cls.url = reverse("customer_list_create")
        cls.customer_data = generate_customer_data()
        cls.customer = Customer.objects.create(**cls.customer_data)

    def test_create_customer(self):
        self.client.force_authenticate(user=self.user)
        test_customer = generate_customer_data()
        response = self.client.post(self.url, test_customer, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Customer.objects.count(), 2)
        created_customer = Customer.objects.get(name=test_customer["name"])
        self.assertEqual(created_customer.name, response.data["name"])

    def test_create_existed_customer(self):
        self.client.force_authenticate(user=self.user)
        existing_customer = generate_customer_data(name=self.customer.name)
        response = self.client.post(self.url, existing_customer, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invalid_email(self):
        self.client.force_authenticate(user=self.user)
        invalid_customer = generate_customer_data(email="longnguyen@@gmail..com")
        response = self.client.post(self.url, invalid_customer, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_invalid_phone_number(self):
        self.client.force_authenticate(user=self.user)
        invalid_customer = generate_customer_data(phone="+1 4710295719")
        response = self.client.post(self.url, invalid_customer, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_customers(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get(self.url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], self.customer.name)
