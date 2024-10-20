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
        if 'WEBSITE_HOSTNAME' in os.environ:
            os.system("python manage.py flush --no-input && python manage.py createsuperuser --username root --email root@pmso.vn --no-input")
        else:
            db_path = os.path.join(settings.BASE_DIR, "db.sqlite3")
            if os.path.exists(db_path):
                os.remove(db_path)
                self.stdout.write(self.style.SUCCESS("Deleted db.sqlite3"))
            self.stdout.write(self.style.WARNING("Running migrations..."))
            os.system("python manage.py migrate")

    def generate_phone_number(self):
        first_digit = "0"
        second_digit = random.choice(["3", "5", "7", "8", "9"])
        remaining_digits = "".join(random.choices("0123456789", k=8))
        return first_digit + second_digit + remaining_digits

    def create_user_data(self):
        roles = get_all_roles_names()
        if 'WEBSITE_HOSTNAME' not in os.environ:
            User.objects.create_superuser(
                username="admin",
                display_name="django-admin",
                password="admin"
            )
            self.stdout.write(self.style.SUCCESS(f"Created 1 admin user: admin/admin"))
        for i in range(20):
            user = User.objects.create_user(
                username=f"user{i}",
                password="password123",
                display_name=f"User {i}",
                phone_number=self.generate_phone_number(),
                address=f"123{i} Main St, City, Country",
                role=random.choice(roles),
                avatar=None,
            )
            self.users.append(user)

        
        self.stdout.write(self.style.SUCCESS(f"Created {len(self.users)} users"))

    def create_customer_data(self):
        for i in range(20):
            num_contacts = random.randint(1, 3)
            default_contact_index = random.randint(0, num_contacts - 1)
            
            contact_list = []
            for j in range(num_contacts):
                contact_list.append({
                    "id": j + 1,
                    "contact": {
                        "is_default": j == default_contact_index,
                        "name": f"Contact {j}",
                        "phone": self.generate_phone_number(),
                        "email": f"contact{j}@example.com",
                        "position": f"Position {j}",
                    }
                })

            customer = Customer.objects.create(
                name=f"Customer {i}",
                phone=self.generate_phone_number(),
                tier=random.choice([choice[0] for choice in get_all_tier_choices()]),
                fax=random.randint(100000, 9999999),
                email=f"customer{i}@example.com",
                address={
                    "home_address": f"{random.randint(1, 100)} Main St",
                    "ward": f"Ward {random.randint(1, 10)}",
                    "district": f"District {random.randint(1, 5)}",
                    "city": f"City {random.randint(1, 3)}",
                    "country": "Vietnam",
                },
                contact_list=contact_list,
            )
            self.customers.append(customer)

        self.stdout.write(
            self.style.SUCCESS(f"Created {len(self.customers)} customers")
        )

    def create_product_data(self):
        categories = [choice[0] for choice in get_all_category_choices()]
        for i in range(30):
            product = Product.objects.create(
                name=f"Product {i}",
                category=random.choice(categories),
                is_active=random.choice([True, False]),
                quantity=random.randint(1, 100),
                price=random.randint(10000000, 100000000),
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
                note="Xin vui lòng lưu ý rằng đơn hàng này cần được giao vào buổi sáng, trước 10 giờ. Khách hàng đã yêu cầu không giao vào cuối tuần. Nếu có bất kỳ vấn đề gì với việc giao hàng, xin vui lòng liên hệ với tôi qua số điện thoại đã cung cấp. Cảm ơn sự hỗ trợ của các bạn!",
                sale_staff=random.choice(self.users),
                logistic_staff=random.choice(self.users),
                deliverer=random.choice(self.users),
            )
            self.orders.append(order)

            current_products = self.products[::]
            for j in range(5):
                chosen_product = random.choice(current_products)
                ProductOrderProduct.objects.create(
                    product_order=order,
                    product=chosen_product,
                    quantity=random.randint(1, 10),
                )
                current_products.remove(chosen_product)

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
