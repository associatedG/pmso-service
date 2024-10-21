from django.urls import path
from .views import (
    UserNotificationListView,
    NotificationDetailView,
    NotificationListView,
)

urlpatterns = [
    path(
        "notifications/", NotificationListView.as_view(), name="notification-list"
    ),  # All notifications
    path(
        "notifications/<int:pk>/",
        NotificationDetailView.as_view(),
        name="notification-detail",
    ),  # Notification by ID
    path(
        "notifications/me/",
        UserNotificationListView.as_view(),
        name="user-notification-list",
    ),  # Notifications for current user
]
