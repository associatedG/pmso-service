from django.urls import path
from .views import (
    ProductOrderListCreateView,
    ProductOrderRetrieveUpdateDestroyView,
    CustomerListCreateView,
)

urlpatterns = [
    path(
        "productorders/<uuid:id>/",
        ProductOrderRetrieveUpdateDestroyView.as_view(),
        name="product_order_detail",
    ),
    path(
        "productorders/",
        ProductOrderListCreateView.as_view(),
        name="product_order_list_create",
    ),
    path(
        "customers/",
        CustomerListCreateView.as_view(),
        name="customer_list_create",
    ),
]
