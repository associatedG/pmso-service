from django.db import models
from django.utils import timezone

class Notification(models.Model):
    product = models.ForeignKey("products.Product", on_delete=models.CASCADE, related_name='notifications', null=True, blank=True)
    product_order = models.ForeignKey("products.ProductOrder", on_delete=models.CASCADE, related_name='notifications', null=True, blank=True)
    message = models.CharField(max_length=255)
    user = models.ForeignKey("account.User", on_delete=models.CASCADE)  # Use User model from account
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"