from django.db import models


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)


class ProductOrder(models.Model):
    URGENT = True
    NOT_URGENT = False

    PRIORITY_CHOICES = {
        (URGENT, 'Urgent'),
        (NOT_URGENT, 'Not Urgent'),
    }

    id = models.AutoField(primary_key=True)
    isUrgent = models.BooleanField(
        choices=PRIORITY_CHOICES,
        default=NOT_URGENT
    )
    dueDate = models.DateField()
    status = models.CharField(max_length=50)
    products = models.ManyToManyField(
        Product,
        through='ProductOrderProduct'
    )
    createdAt = models.DateTimeField(auto_now_add=True)


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

