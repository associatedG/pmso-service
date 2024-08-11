from django.urls import path
from .views import ProductOrderListCreateView, ProductOrderRetrieveUpdateDestroyView

urlpatterns = [
    # ProductOrder endpoints
    path(
        "product-orders/<uuid:id>/",
        ProductOrderRetrieveUpdateDestroyView.as_view(),
        name="product_order_detail",
    ),
    path(
        "product-orders/",
        ProductOrderListCreateView.as_view(),
        name="product_order_list_create",
    ),
]
