from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from .models import Notification
from .serializers import NotificationSerializer


class NotificationListView(generics.ListAPIView):
    """
    View to retrieve all notifications.
    """

    serializer_class = NotificationSerializer

    def get_queryset(self):
        MAX_READ_NOTIFICATION = 10
        # Fetch all unread notifications
        unread_notifications = Notification.objects.filter(is_read=False).order_by(
            "-created_at"
        )

        # Fetch read notifications, limited to a total of 10 notifications
        read_notifications = Notification.objects.filter(is_read=True).order_by(
            "-created_at"
        )

        # return read count
        total_read_noti_return = max(
            0, MAX_READ_NOTIFICATION - len(unread_notifications)
        )

        # Combine the two querysets
        combined_notifications = (
            list(unread_notifications)
            + list(read_notifications)[:total_read_noti_return]
        )
        combined_notifications_sorted = sorted(
            combined_notifications, key=lambda x: x.created_at, reverse=True
        )

        return combined_notifications_sorted

    # permission_classes = [IsAuthenticated]


class UserNotificationListView(generics.ListAPIView):
    """
    View to retrieve notifications for the authenticated user.
    """

    serializer_class = NotificationSerializer
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Retrieve notifications for the authenticated user
        return Notification.objects.filter(user=self.request.user)


class NotificationDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    View to retrieve a specific notification by ID.
    """

    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    # permission_classes = [IsAuthenticated]

    def get_object(self):
        try:
            return super().get_object()
        except Notification.DoesNotExist:
            raise NotFound("Notification not found.")
