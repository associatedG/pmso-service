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

""" 
The following API route is designed to retrieve a list of all products in the database.
The route is defined at the endpoint '/products/' and is accessible via a GET request.
When this endpoint is hit, the ProductListView class-based view is invoked.

The response from this API will be a JSON array serialized using ProductSerializer, where each element in the array represents
a single product. Each product object in the array will include the following fields:
1. id: uuid
2. name: string
3. category: string(choice)
4. quantity: unsigned integer
5. price: unsigned integer
6. created_at: DateTime
7. updated_at: DateTime
"""
