import random
import string
from django.utils import timezone
from datetime import timedelta
from utils.choices_utils import get_all_category_choices, get_all_status_choices

CATEGORY_CHOICES = get_all_category_choices()
STATUS_CHOICES = get_all_status_choices()


def generate_random_string(length=10):
    """Generate a random string of a given length."""
    letters = string.ascii_letters + string.digits
    return "".join(random.choice(letters) for _ in range(length))


def generate_phone_number():
    """Generate a random phone number"""
    return f"0{random.choice('35789')}{random.randint(10000000, 99999999)}"


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
        "status": random.choice([status for status in STATUS_CHOICES])[0],
        "customer": customer_id,
        "sale_staff": staff_id,
        "logistic_staff": staff_id,
        "deliverer": staff_id,
        "products": products,
    }


def mock_user_generator(
    username=None,
    password=None,
    display_name=None,
    phone_number=None,
    address=None,
    role="SALE_STAFF",
):
    """Generate mock user based on role"""
    return {
        "username": username or generate_random_string(),
        "password": password or generate_random_string(),
        "display_name": display_name or generate_random_string(),
        "phone_number": phone_number or "+840912345678",
        "address": address or generate_random_string(),
        "role": role,
    }
