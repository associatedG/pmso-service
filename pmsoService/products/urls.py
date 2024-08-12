from django.urls import path
from .views import ProductOrderListCreateView, ProductListCreateView, ProductRetrieveUpdateDestroyView, ProductOrderRetrieveUpdateDestroyView, ProductOrderProductListCreateView,ProductOrderProductRetrieveUpdateDestroyView

urlpatterns = [
    path(
        "product-orders-product/<uuid:id>/",
        ProductOrderProductRetrieveUpdateDestroyView.as_view(),
        name="product_order_detail",
    ),
    path(
        "product-orders-product/",
        ProductOrderProductListCreateView.as_view(),
        name="product_order_list_create",
    ),
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
