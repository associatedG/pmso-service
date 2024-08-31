import os
import random
from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone
from products.models import Customer, Product, ProductOrder, ProductOrderProduct
from account.models import User
from utils.choices_utils import (
    get_all_tier_choices,
    get_all_status_choices,
    get_all_category_choices,
)
from utils.roles_utils import get_all_roles_names


class Command(BaseCommand):
    help = "Populates the database with initial data"

    def delete_and_create_data_base(self):
        db_path = os.path.join(settings.BASE_DIR, 'db.sqlite3')
        if os.path.exists(db_path):
            os.remove(db_path)
            self.stdout.write(self.style.SUCCESS('Deleted db.sqlite3'))
        self.stdout.write(self.style.WARNING('Running migrations...'))
        os.system('python manage.py migrate')

    def generate_phone_number(self):
        first_digit = "0"
        second_digit = random.choice(["3", "5", "7", "8", "9"])
        remaining_digits = "".join(random.choices("0123456789", k=8))
        return first_digit + second_digit + remaining_digits

    def create_user_data(self):
        roles = get_all_roles_names()
        for i in range(20):
            user = User.objects.create_user(
                username=f"user{i}",
                password="password123",
                display_name=f"User {i}",
                phone_number= self.generate_phone_number(),
                address=f"123{i} Main St, City, Country",
                role=random.choice(roles),
                avatar=None,
            )
            self.users.append(user)

        self.stdout.write(self.style.SUCCESS(f"Created {len(self.users)} users"))

    def create_customer_data(self):
        for i in range(20):
            customer = Customer.objects.create(
                name=f"Customer {i}",
                phone=self.generate_phone_number(),
                tier=random.choice([choice[0] for choice in get_all_tier_choices()]),
                fax=random.randint(1000000000, 9999999999),
                email=f"customer{i}@example.com",
                address=f"1234 Address St, City {i}, Country",
                note=f"This is a note for Customer {i}",
                contact_list={
                    "primary": f"contact{i}@example.com",
                    "secondary": f"secondary{i}@example.com",
                },
            )
            self.customers.append(customer)

        self.stdout.write(self.style.SUCCESS(f"Created {len(self.customers)} customers"))

    def create_product_data(self):
        categories = [choice[0] for choice in get_all_category_choices()]
        for i in range(30):
            product = Product.objects.create(
                name=f"Product {i}",
                category=random.choice(categories),
                quantity=random.randint(1, 100),
                price=random.randint(10, 500),
            )
            self.products.append(product)

        self.stdout.write(self.style.SUCCESS(f"Created {len(self.products)} products"))

    def create_product_order_with_status_data(self, status):
        for i in range(5):
            order = ProductOrder.objects.create(
                name=f"Order_{status}_{i}",
                is_urgent=random.choice([True, False]),
                due_date=timezone.now().date()
                         + timezone.timedelta(days=random.randint(1, 30)),
                status=status,
                customer=random.choice(self.customers),
                sale_staff=random.choice(self.users),
                logistic_staff=random.choice(self.users),
                deliverer=random.choice(self.users),
            )
            self.orders.append(order)

            for j in range(5):
                ProductOrderProduct.objects.create(
                    product_order=order,
                    product=random.choice(self.products),
                    quantity=random.randint(1, 10),
                )

        self.stdout.write(
            self.style.SUCCESS(f"Created 5 '{status}' orders with products")
        )

    def create_product_order_data(self):
        for choice in get_all_status_choices():
            self.create_product_order_with_status_data(choice[0])

    def handle(self, *args, **kwargs):
        self.users = []
        self.customers = []
        self.products = []
        self.orders = []

        self.delete_and_create_data_base()
        self.create_user_data()
        self.create_customer_data()
        self.create_product_data()
        self.create_product_order_data()

