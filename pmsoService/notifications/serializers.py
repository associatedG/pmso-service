from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'target_url', 'target_name', 'message', 'user', 'created_at', "actor", "action", "is_read"]