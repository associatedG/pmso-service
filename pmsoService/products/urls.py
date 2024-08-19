from django.urls import path
from .views import (
    ProductOrderListCreateView,
    ProductOrderRetrieveUpdateDestroyView,
    ProductListCreateAPIView,
    ProductRetrieveUpdateDestroyAPIView,
    CustomerListCreateView,
    CustomerDetail,
)

urlpatterns = [
    path(
         "products/",
         ProductListCreateAPIView.as_view(),
         name='product_list_create'
    ),
    path(
        "products/<uuid:id>",
        ProductRetrieveUpdateDestroyAPIView.as_view(),
        name='product_detail'
    ),
    path(
        "product/orders/<uuid:id>/",
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
    path(
        "customers/<uuid:id>/",
        CustomerDetail.as_view(),
        name="customer_detail_update_destroy",
    ),
]
