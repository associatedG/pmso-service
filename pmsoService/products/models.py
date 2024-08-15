from django.utils import timezone
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
import uuid


class Customer(models.Model):
    TIER_1 = "T1"
    TIER_2 = "T2"
    TIER_3 = "T3"

    TIER_CHOICES = [
        (TIER_1, "Cấp độ 1"),
        (TIER_2, "Cấp độ 2"),
        (TIER_3, "Cấp độ 3"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True, blank=True, null=True)
    phone = models.CharField(max_length=10, blank=True, null=True)
    tier = models.CharField(max_length=50, choices=TIER_CHOICES, default=TIER_1)
    fax = models.IntegerField(blank=True, null=True)
    contact_list = models.JSONField(blank=True, null=True, default=dict)
    email = models.EmailField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name = "Customer"
        verbose_name_plural = "Customers"


class Product(models.Model):
    CATEGORY_TYPE_ONE = "Phuy"
    CATEGORY_TYPE_TWO = "Thùng"
    CATEGORY_TYPE_THREE = "Cơ Khí Ô Tô"

    CATEGORY_CHOICES = [
        (CATEGORY_TYPE_ONE, "Phuy"),
        (CATEGORY_TYPE_TWO, "Thùng"),
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
        choices=CATEGORY_CHOICES,
    )
    quantity = models.PositiveIntegerField()
    price = models.PositiveIntegerField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name = "Product"
        verbose_name_plural = "Products"


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
    name = models.CharField(max_length=255, unique=True, blank=True, null=True)
    is_urgent = models.BooleanField(default=False)
    due_date = models.DateField()
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default=OPEN)
    created_at = models.DateTimeField(default=timezone.now)
    last_modified = models.DateTimeField(auto_now=True, null=True)
    customer = models.ForeignKey(
        "Customer",
        on_delete=models.PROTECT,
        null=True,
        related_name="orders",
    )
    sale_staff = models.ForeignKey(
        "account.User",
        on_delete=models.PROTECT,
        null=True,
        related_name="sale_orders",
    )
    logistic_staff = models.ForeignKey(
        "account.User",
        on_delete=models.PROTECT,
        null=True,
        related_name="logistic_orders",
    )
    deliverer = models.ForeignKey(
        "account.User",
        on_delete=models.PROTECT,
        null=True,
        related_name="delivery_orders",
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["due_date"]
        verbose_name = "Product Order"
        verbose_name_plural = "Product Orders"


class ProductOrderProduct(models.Model):
    product_order = models.ForeignKey(
        ProductOrder, on_delete=models.CASCADE, related_name="products"
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.product_order.name} - {self.product.name}"

    class Meta:
        verbose_name = "Product Order Product"
        verbose_name_plural = "Product Order Products"
