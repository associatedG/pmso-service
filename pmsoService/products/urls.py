from django.urls import path
from .views import (
    ProductListCreateView, ProductRetrieveUpdateDestroyView,
    ProductOrderListCreateView, ProductOrderRetrieveUpdateDestroyView,
    ProductOrderProductListCreateView, ProductOrderProductRetrieveUpdateDestroyView
)

urlpatterns = [
    # Product endpoints
    path('products/<uuid:id>/',
         ProductRetrieveUpdateDestroyView.as_view(),
         name='product_detail'),
    path('products/',
         ProductListCreateView.as_view(),
         name='product_list_create'),


    # ProductOrder endpoints
    path('productorders/<uuid:id>/',
         ProductOrderRetrieveUpdateDestroyView.as_view(),
         name='product_order_detail'),

    path('productorders/',
         ProductOrderListCreateView.as_view(),
         name='product_order_list_create'),

    # ProductOrderProduct endpoints
    path('productorderproducts/<int:pk>/',
         ProductOrderProductRetrieveUpdateDestroyView.as_view(), name='product_order_product_detail'),

    path('productorderproducts/', ProductOrderProductListCreateView.as_view(), name='product_order_product_list_create'),


]
