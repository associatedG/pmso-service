from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from products.models import Customer


class CustomerListCreateViewTest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()
        cls.url = reverse("customer_list_create")
        cls.initial_data = {
            "name": "Existing User",
            "email": "existinguser@example.com",
            "phone": "+84 987654321",
        }
        cls.customer = Customer.objects.create(**cls.initial_data)

    def test_create_customer(self):
        new_customer_data = {
            "name": "John Doe",
            "email": "johndoe@example.com",
            "phone": "+84 865640601",
        }
        response = self.client.post(self.url, new_customer_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Customer.objects.count(), 2)
        self.assertEqual(Customer.objects.get(name="John Doe").name, "John Doe")

    def test_list_customers(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "Existing User")
