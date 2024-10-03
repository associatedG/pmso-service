from django.utils import timezone
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from utils.choices_utils import *
import uuid
import json
import os
from notifications.models import Notification
from account.models import User

TIER_CHOICES = get_all_tier_choices()
STATUS_CHOICES = get_all_status_choices()
CATEGORY_CHOICES = get_all_category_choices()


class Customer(models.Model):
    id = models.UUIDField(
        primary_key=True, unique=True, default=uuid.uuid4, editable=False
    )
    name = models.CharField(max_length=255, unique=True, blank=False, null=False)
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
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    is_active = models.BooleanField(default=True)
    name = models.CharField(max_length=255, unique=True, blank=False, null=False)
    category = models.CharField(
        max_length=255,
        choices=CATEGORY_CHOICES,
    )
    quantity = models.PositiveIntegerField()
    price = models.PositiveIntegerField()

    def save(self, *args, **kwargs):
        action = "updated" if self.pk else "created"
        super().save(*args, **kwargs)

        # Create notifications
        self.create_notifications(action)

    def delete(self, *args, **kwargs):
        # Create a notification for deletion
        Notification.objects.create(
            product=self,
            message=f'Product {self.name} has been deleted.',
            #user=self.sale_staff  # Example: Notify sale staff
        )
        super().delete(*args, **kwargs)

    def create_notifications(self, action):
        # Get all relevant users to notify
        users_to_notify = set()

        # Notify admin users (you can customize this logic as per your role management)
        admin_users = User.objects.filter(role='ADMIN')
        users_to_notify.update(admin_users)

        for user in users_to_notify:
            Notification.objects.create(
                product=self,
                message=f'Product {self.name} has been {action}.',
                user=user
            )

    class Meta:
        ordering = ["name"]
        verbose_name = "Product"
        verbose_name_plural = "Products"


class ProductOrder(models.Model):
    OPEN = STATUS_CHOICES[0][0]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, blank=True, null=False)
    is_urgent = models.BooleanField(default=False)
    due_date = models.DateField()
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default=OPEN)
    note = models.CharField(max_length=2000, blank=True, default="")
    is_cancelled = models.BooleanField(default=False)
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

    def save(self, *args, **kwargs):
        action = "updated" if self.pk else "created"
        super().save(*args, **kwargs)

        # Create notifications
        self.create_notifications(action)

    def delete(self, *args, **kwargs):
        # Create a notification for deletion
        Notification.objects.create(
            product_order=self,
            message=f'Product Order {self.name} has been deleted.',
            user=self.sale_staff  # Example: Notify sale staff
        )
        super().delete(*args, **kwargs)

    def create_notifications(self, action):
        # Get all relevant users to notify
        users_to_notify = set()

        # Notify sale staff, logistic staff, and deliverer
        if self.sale_staff:
            users_to_notify.add(self.sale_staff)
        if self.logistic_staff:
            users_to_notify.add(self.logistic_staff)
        if self.deliverer:
            users_to_notify.add(self.deliverer)

        # Notify admin users
        admin_users = User.objects.filter(role='ADMIN')
        users_to_notify.update(admin_users)

        for user in users_to_notify:
            Notification.objects.create(
                product_order=self,
                message=f'Product Order {self.name} has been {action}.',
                user=user
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
