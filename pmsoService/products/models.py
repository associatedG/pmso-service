from django.utils import timezone
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from utils.choices_utils import *
import uuid
from django.core.exceptions import ObjectDoesNotExist

TIER_CHOICES = get_all_tier_choices()
STATUS_CHOICES = get_all_status_choices()
CATEGORY_CHOICES = get_all_category_choices()

class Customer(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4, editable=False)
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
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    is_active = models.BooleanField(default=True)
    name = models.CharField(max_length=255, unique=True, blank=False, null=False)
    category = models.CharField(max_length=255, choices=CATEGORY_CHOICES)
    quantity = models.PositiveIntegerField()
    price = models.PositiveIntegerField()
    
    _previous_state = None  # Attribute to hold previous state

    def save(self, user=None, *args, **kwargs):
        # Fetch previous state before saving
        try:
            previous_state = ProductOrder.objects.get(pk=self.pk)
            self._previous_state = previous_state
        except:
            self._previous_state = None
        
        # Save the current state
        super().save(*args, **kwargs)
        # Notify with the user after saving
        if user:
            # Call the post_save signal handler manually if needed
            product_saved(sender=self.__class__, instance=self, created=(self.pk is None), user=user)

    def get_changes(self):
        changes = []
        if self._previous_state:
            for field in self._meta.fields:
                # Skip fields you don't want to log
                if field.name in ['created_at', 'last_modified']:
                    continue
                
                old_value = getattr(self._previous_state, field.name)
                new_value = getattr(self, field.name)
                if old_value != new_value:
                    changes.append(f"{field.name}={old_value} -> {new_value}")
        return changes

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
    customer = models.ForeignKey("Customer", on_delete=models.PROTECT, null=True, related_name="orders")
    sale_staff = models.ForeignKey("account.User", on_delete=models.PROTECT, null=True, related_name="sale_orders")
    logistic_staff = models.ForeignKey("account.User", on_delete=models.PROTECT, null=True, related_name="logistic_orders")
    deliverer = models.ForeignKey("account.User", on_delete=models.PROTECT, null=True, related_name="delivery_orders")
    
    _previous_state = None  # Attribute to hold previous state

    def save(self, user=None, *args, **kwargs):
        # Fetch previous state before saving
        try:
            previous_state = ProductOrder.objects.get(pk=self.pk)
            self._previous_state = previous_state
        except:
            self._previous_state = None
        
        # Save the current state
        super().save(*args, **kwargs)

        # Notify with the user after saving
        if user:
            # Call the post_save signal handler manually if needed
            product_saved(sender=self.__class__, instance=self, created=(self.pk is None), user=user)
        

    def get_changes(self):
        changes = []
        if self._previous_state:
            for field in self._meta.fields:
                # Skip fields you don't want to log
                if field.name in ['created_at', 'last_modified']:
                    continue
                
                old_value = getattr(self._previous_state, field.name)
                new_value = getattr(self, field.name)
                if old_value != new_value:
                    changes.append(f"{field.name}={old_value} -> {new_value}")
        return changes

    class Meta:
        ordering = ["due_date"]
        verbose_name = "Product Order"
        verbose_name_plural = "Product Orders"


class ProductOrderProduct(models.Model):
    product_order = models.ForeignKey(ProductOrder, on_delete=models.CASCADE, related_name="products")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    class Meta:
        verbose_name = "Product Order Product"
        verbose_name_plural = "Product Order Products"
