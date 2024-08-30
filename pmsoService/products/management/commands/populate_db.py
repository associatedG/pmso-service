import random
from django.core.management.base import BaseCommand
from django.utils import timezone
from products.models import Customer, Product, ProductOrder, ProductOrderProduct
from account.models import User
from utils.choices_utils import get_all_tier_choices, get_all_status_choices, get_all_category_choices
from utils.roles_utils import get_all_roles_names

class Command(BaseCommand):
    help = 'Populates the database with initial data'

    def handle(self, *args, **kwargs):
        ProductOrderProduct.objects.all().delete()
        ProductOrder.objects.all().delete()
        Customer.objects.all().delete()
        Product.objects.all().delete()
        User.objects.all().delete()

        users = []
        roles = get_all_roles_names()
        for i in range(20):
            user = User.objects.create_user(
                username=f'user{i}',
                password='password123',
                display_name=f'User {i}',
                phone_number=f'+123456789{i}',
                address=f'123{i} Main St, City, Country',
                role=random.choice(roles),
                avatar=None
            )
            users.append(user)

        self.stdout.write(self.style.SUCCESS(f'Created {len(users)} users'))

        customers = []
        for i in range(20):
            customer = Customer.objects.create(
                name=f'Customer {i}',
                phone=f'{random.randint(1000000000, 9999999999)}',
                tier=random.choice([choice[0] for choice in get_all_tier_choices()]),
                fax=random.randint(1000000000, 9999999999),
                email=f'customer{i}@example.com',
                address=f'1234 Address St, City {i}, Country',
                note=f'This is a note for Customer {i}',
                contact_list={"primary": f"contact{i}@example.com", "secondary": f"secondary{i}@example.com"},
            )
            customers.append(customer)

        self.stdout.write(self.style.SUCCESS(f'Created {len(customers)} customers'))

        products = []
        categories = [choice[0] for choice in get_all_category_choices()]
        for i in range(30):
            product = Product.objects.create(
                name=f'Product {i}',
                category=random.choice(categories),
                quantity=random.randint(1, 100),
                price=random.randint(10, 500),
            )
            products.append(product)

        self.stdout.write(self.style.SUCCESS(f'Created {len(products)} products'))

        orders = []
        statuses = [choice[0] for choice in get_all_status_choices()]
        for i in range(30):
            order = ProductOrder.objects.create(
                name=f'Order {i}',
                is_urgent=random.choice([True, False]),
                due_date=timezone.now().date() + timezone.timedelta(days=random.randint(1, 30)),
                status=random.choice(statuses),
                customer=random.choice(customers),
                sale_staff=random.choice(users),
                logistic_staff=random.choice(users),
                deliverer=random.choice(users),
            )
            orders.append(order)

            for j in range(random.randint(20, 30)):
                ProductOrderProduct.objects.create(
                    product_order=order,
                    product=random.choice(products),
                    quantity=random.randint(1, 10),
                )

        self.stdout.write(self.style.SUCCESS(f'Created {len(orders)} orders with products'))
