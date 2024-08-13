from django.utils import timezone
from django.db import models
import uuid


class Product(models.Model):
    CATEGORY_TYPE_ONE = "Phuy"
    CATEGORY_TYPE_TWO = "Thung"
    CATEGORY_TYPE_THREE = "Cơ Khí Ô Tô"

    CATEGORY_CHOICE = [
        (CATEGORY_TYPE_ONE, "Phuy"),
        (CATEGORY_TYPE_TWO, "Thung"),
        (CATEGORY_TYPE_THREE, "Cơ Khí Ô Tô"),
    ]

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    name = models.CharField(max_length=255, unique=True, blank=True, null=True)
    category = models.CharField(
        max_length=255,
        choices=CATEGORY_CHOICE,
    )
    quantity = models.PositiveIntegerField()
    price = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class ProductOrder(models.Model):
    OPEN = "Open"
    PLANNING_PRODUCTION = "Planning Production"
    IN_PRODUCTION = "In Production"
    DELIVERING = "Delivering"
    COMPLETED = "Completed"

    STATUS_CHOICES = [
        (OPEN, "Mở"),
        (PLANNING_PRODUCTION, "Lên Kế Hoạch Sản Xuất"),
        (IN_PRODUCTION, "Đang Sản Xuất"),
        (DELIVERING, "Giao Hàng"),
        (COMPLETED, "Hoàn Thành"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    is_urgent = models.BooleanField(default=False)
    due_date = models.DateField()
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default=OPEN)
    created_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True, null=True)

    sale_staff = models.ForeignKey(
        "account.User",
        on_delete=models.RESTRICT,
        null=True,
        related_name="sale_orders",
    )
    logistic_staff = models.ForeignKey(
        "account.User",
        on_delete=models.RESTRICT,
        null=True,
        related_name="logistic_orders",
    )
    deliverer = models.ForeignKey(
        "account.User",
        on_delete=models.RESTRICT,
        null=True,
        related_name="delivery_orders",
    )


class ProductOrderProduct(models.Model):
    product_order = models.ForeignKey(ProductOrder, on_delete=models.CASCADE, related_name='products')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
