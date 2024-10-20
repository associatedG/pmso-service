from django.db import models
from django.utils import timezone

class Notification(models.Model):
    target_url = models.CharField(max_length=2000, blank=True, null=True)
    target_name = models.CharField(max_length=2000, blank=True, null=True)
    message = models.CharField(max_length=2000)
    changes = models.CharField(max_length=2000)
    user = models.ForeignKey("account.User", on_delete=models.CASCADE)  # Use User model from account
    actor = models.ForeignKey("account.User", on_delete=models.CASCADE, related_name='notifications_sent', null=True)  # User who performed the action
    created_at = models.DateTimeField(default=timezone.now)
    action = models.CharField(max_length=20)  # New action field
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.target_name}: {self.action} notification for {self.user}"

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"