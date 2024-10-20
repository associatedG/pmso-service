from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from .models import Notification
from .serializers import NotificationSerializer

class NotificationListView(generics.ListAPIView):
    """
    View to retrieve all notifications.
    """
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    #permission_classes = [IsAuthenticated]

class UserNotificationListView(generics.ListAPIView):
    """
    View to retrieve notifications for the authenticated user.
    """
    serializer_class = NotificationSerializer
    #permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Retrieve notifications for the authenticated user
        return Notification.objects.filter(user=self.request.user)

class NotificationDetailView(generics.RetrieveAPIView):
    """
    View to retrieve a specific notification by ID.
    """
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    #permission_classes = [IsAuthenticated]

    def get_object(self):
        try:
            return super().get_object()
        except Notification.DoesNotExist:
            raise NotFound("Notification not found.")
