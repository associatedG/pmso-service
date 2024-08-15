from django.urls import path
from .views import (
    ProductOrderListCreateView,
    ProductOrderRetrieveUpdateDestroyView,
    ProductListCreateView,
    CustomerListCreateView,
)

urlpatterns = [
    path(
        "products/",
         ProductListCreateView.as_view(),
         name="product_list_create",
    ),
    path(
        "products/orders/<uuid:id>/",
        ProductOrderRetrieveUpdateDestroyView.as_view(),
        name="product_order_detail",
    ),
    path(
        "products/orders",
        ProductOrderListCreateView.as_view(),
        name="product_order_list_create",
    ),
    path(
        "customers/",
        CustomerListCreateView.as_view(),
        name="customer_list_create",
    ),
]
