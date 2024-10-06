from django.urls import path
from .views import NotificationListView, UserNotificationListView

urlpatterns = [
    path('notifications/', NotificationListView.as_view(), name='notification-list'),
    path('notifications/me/', UserNotificationListView.as_view(), name='user-notification-list'),
]