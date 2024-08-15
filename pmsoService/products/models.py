from django.utils import timezone
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
import uuid
import json
import os

with open('config/choices_config.json') as choices_config:
    CHOICES = json.load(choices_config)

class Customer(models.Model):
    TIER_CHOICES = CHOICES["CUSTOMER"]["TIER_CHOICES"]

    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True, blank=True, null=True)
    phone = models.CharField(max_length=10, blank=True, null=True)
    tier = models.CharField(max_length=50, choices=TIER_CHOICES)
    fax = models.IntegerField(blank=True, null=True)
    contact_list = models.JSONField(blank=True, null=True, default=dict)
    email = models.EmailField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Customer"
        verbose_name_plural = "Customers"


class Product(models.Model):
    CATEGORY_CHOICES = CHOICES["PRODUCT"]["CATEGORY_CHOICES"]

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

    class Meta:
        ordering = ["name"]
        verbose_name = "Product"
        verbose_name_plural = "Products"


class ProductOrder(models.Model):
    STATUS_CHOICES = CHOICES["PRODUCT_ORDER"]["STATUS_CHOICES"]
    OPEN = STATUS_CHOICES[0][0]

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

    class Meta:
        verbose_name = "Product Order Product"
        verbose_name_plural = "Product Order Products"
