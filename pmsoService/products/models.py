from django.db import models


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)


class ProductOrder(models.Model):
    id = models.AutoField(primary_key=True)
    isUrgent = models.BooleanField(default=False)
    dueDate = models.DateField()
    status = models.CharField(max_length=50)
    createdAt = models.DateTimeField(auto_now_add=True)
