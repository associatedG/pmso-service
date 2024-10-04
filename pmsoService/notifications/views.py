from rest_framework import generics
from .models import Notification
from .serializers import NotificationSerializer
#from rest_framework.permissions import IsAuthenticated

class NotificationListView(generics.ListAPIView):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

class UserNotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    #permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)
