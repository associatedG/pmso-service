from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model
import uuid
import string
import random

User = get_user_model()

def generate_random_string(length=10):
    """Generate a random string of a given length."""
    letters = string.ascii_letters + string.digits
    return "".join(random.choice(letters) for _ in range(length))


def mock_user_generator(role="SALE_STAFF"):
    """Generate mock user based on role"""
    return {
        "username": generate_random_string(),
        "password": generate_random_string(),
        "display_name": generate_random_string(),
        "phone_number": "+840912345678",
        "address": generate_random_string(),
        "role": role,
    }


class TestUserView(APITestCase):

    @classmethod
    def setUpTestData(self):
        self.user = User.objects.create_user(username="test", password="test123")
        self.client = APIClient()

    def test_get_existed_user(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(
            reverse("user_update_retrieve", kwargs={"id": self.user.id}),
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_non_existed_user(self):
        self.client.force_authenticate(user=self.user)
        non_existed_id = uuid.uuid4()
        response = self.client.get(
            reverse("user_update_retrieve", kwargs={"id": non_existed_id}),
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_existed_user(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(
            reverse("user_update_retrieve", kwargs={"id": self.user.id}),
            {"username": "Triet1"},
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_non_existed_user(self):
        self.client.force_authenticate(user=self.user)
        non_existed_id = uuid.uuid4()
        response = self.client.patch(
            reverse("user_update_retrieve", kwargs={"id": non_existed_id}),
            {"username": "Triet1"},
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_user(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            reverse(
                "user_list_create",
            ),
            mock_user_generator(),
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_user_with_incorrect_role(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            reverse(
                "user_list_create",
            ),
            mock_user_generator("WRONG ROLE"),
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_is_active_by_default(self):
        """Test that a new user is active by default."""
        self.assertTrue(self.user.is_active)

    def test_deactivate_user(self):
        """Test deactivating a user."""
        self.user.deactivate()
        self.assertFalse(self.user.is_active)
