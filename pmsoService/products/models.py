from django.utils import timezone
from django.db import models
import uuid


class Product(models.Model):
    CATEGORY_TYPE_ONE = 'Phuy'
    CATEGORY_TYPE_TWO = 'Thung'
    CATEGORY_TYPE_THREE = 'Cơ Khí Ô Tô'

    CATEGORY_CHOICE = [
        (CATEGORY_TYPE_ONE, 'Phuy'),
        (CATEGORY_TYPE_TWO, 'Thung'),
        (CATEGORY_TYPE_THREE, 'Cơ Khí Ô Tô')
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(
        max_length=255,
        unique=True,
        blank=True,
        null=True
    )
    category = models.CharField(
        max_length=255,
        choices=CATEGORY_CHOICE,
    )
    quantity = models.PositiveIntegerField()
    price = models.PositiveIntegerField()


class ProductOrder(models.Model):
    OPEN = 'Open'
    PLANNING_PRODUCTION = 'Planning Production'
    IN_PRODUCTION = 'In Production'
    DELIVERING = 'Delivering'
    COMPLETED = 'Completed'

    STATUS_CHOICES = [
        (OPEN, 'Mở'),
        (PLANNING_PRODUCTION, 'Lên Kế Hoạch Sản Xuất'),
        (IN_PRODUCTION, 'Đang Sản Xuất'),
        (DELIVERING, 'Giao Hàng'),
        (COMPLETED, 'Hoàn Thành')
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    is_urgent = models.BooleanField(default=False)
    dueDate = models.DateField()
    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default=OPEN
    )
    createdAt = models.DateTimeField(auto_now_add=True)
    lastModified = models.DateTimeField(auto_now_add=True, null=True)


class ProductOrderProduct(models.Model):
    product_orders = models.ForeignKey(
        ProductOrder,
        on_delete=models.CASCADE
    )
    products = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField()

