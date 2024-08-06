from django.urls import path
from .views import UserRetrieveUpdateDestroyAPIView, UserListCreateView


urlpatterns = [
    path(
        "<uuid:id>/",
        UserRetrieveUpdateDestroyAPIView.as_view(),
        name="user_update_retrieve",
    ),
    path("", UserListCreateView.as_view(), name="user_list_create"),
]
