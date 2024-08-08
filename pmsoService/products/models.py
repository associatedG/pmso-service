from django.db import models


class ProductOrder(models.Model):
    id = models.AutoField(primary_key=True)
    isUrgent = models.BooleanField(default=False)
    dueDate = models.DateField()
    status = models.CharField(max_length=50)
    createdAt = models.DateTimeField(auto_now_add=True)
