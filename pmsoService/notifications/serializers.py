from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'product', 'product_order', 'message', 'user', 'created_at', "actor", "action"]