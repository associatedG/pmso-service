from django.urls import path
from .views import ProductOrderListCreateView, ProductListCreateView, ProductRetrieveUpdateDestroyView, ProductOrderRetrieveUpdateDestroyView, ProductOrderProductListCreateView,ProductOrderProductRetrieveUpdateDestroyView

urlpatterns = [
    path(
        "<uuid:id>/",
        ProductOrderRetrieveUpdateDestroyView.as_view(),
        name="product_order_detail",
    ),
    path(
        "",
        ProductOrderListCreateView.as_view(),
        name="product_order_list_create",
    ),
    path(
        "products/<uuid:id>/",
        ProductRetrieveUpdateDestroyView.as_view(),
        name="products_detail",
    ),
    path(
        "products/",
        ProductListCreateView.as_view(),
        name="product_list_create",
    ),
]
