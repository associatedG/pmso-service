from django.urls import path
from .views import ProductOrderListCreateView, ProductOrderRetrieveUpdateDestroyView

urlpatterns = [
    # ProductOrder endpoints
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
]
