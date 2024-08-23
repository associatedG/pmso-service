from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework import status,generics
from rest_framework.response import Response

from .filters import ProductOrderFilter, ProductFilter
from .models import Product, ProductOrder, ProductOrderProduct, Customer
from .serializers import (
    ProductSerializer,
    ProductOrderSerializer,
    CustomerSerializer,
)

class ProductOrderPagination(PageNumberPagination):
    page_size = "10"

class ProductPagination(PageNumberPagination):
    page_size = '10'

"""
        GET: /api/products/?category=Phuy&ordering=quantity
        {
            "count": 3,
            "next": null,
            "previous": null,
            "results": [
                {
                    "id": "094df9db-15ab-47fe-9b25-159418db7e26",
                    "name": "Test Phuy 2",
                    "is_active": False,
                    "category": "Phuy",
                    "quantity": 2,
                    "price": 1
                },
                {
                    "id": "f1d30788-7c2e-45d1-b033-ef734c54d98a",
                    "name": "Test Phuy 3",
                    "is_active": True,
                    "category": "Phuy",
                    "quantity": 2,
                    "price": 1
                },
                {
                    "id": "8cd1f3bc-bd2e-4fbc-963f-2f4b0e2b35de",
                    "name": "Test Phuy 1",
                    "is_active": True,
                    "category": "Phuy",
                    "quantity": 5,
                    "price": 5
                }
            ]
        }
        POST:
        {
            "is_active": True,
            "name": "",
            "category": null,
            "quantity": null,
            "price": null
        }
"""

class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["name"]
    filterset_class = ProductFilter
    ordering_fields = ["is_active", "name", "quantity", "price"]
    pagination_class = ProductPagination

class ProductRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "id"

"""
    GET: /api/products/orders?is_urgent=true&due_date__gte=&due_date__lte=&due_date=2024-08-31&status=Open
    {
        "count": 1,
        "next": null,
        "previous": null,
        "results": [
            {
                "id": "3ec930fe-25e5-4f98-8e6c-3208d2e65053",
                "is_urgent": true,
                "due_date": "2024-08-31",
                "status": "Open",
                "customer": "65748bd2-9ab4-490e-b124-bcc6b64bc348",
                "sale_staff": "3a2e5c7c-4231-4fa0-852e-a28aaad21c22",
                "logistic_staff": "3a2e5c7c-4231-4fa0-852e-a28aaad21c22",
                "deliverer": "3a2e5c7c-4231-4fa0-852e-a28aaad21c22",
                "last_modified": "2024-08-21T17:42:40.810884Z",
                "created_at": "2024-08-21T17:42:11Z",
                "products": [
                    {
                        "product": {
                            "id": "b516c4f1-7be0-4372-848c-9fb08c858a7d",
                            "name": "Test Bon Xitec",
                            "category": "Cơ Khí Ô Tô",
                            "quantity": 7,
                            "price": 5
                        },
                        "quantity": 1
                    },
                    {
                        "product": {
                            "id": "8cd1f3bc-bd2e-4fbc-963f-2f4b0e2b35de",
                            "name": "Test Phuy 1",
                            "category": "Phuy",
                            "quantity": 5,
                            "price": 5
                        },
                        "quantity": 1
                    }
                ]
            }
        ]
    }
    POST:
    {
        "is_urgent": true,
        "due_date": "2025-08-23",
        "status": "Open",
        "customer": "d3e047a3-a71a-4d03-86a1-43914455ac18",
        "sale_staff": "fd66f621-1f79-45c8-bd89-c0c5ac11b2d8",
        "logistic_staff": "fd66f621-1f79-45c8-bd89-c0c5ac11b2d8",
        "deliverer": "fd66f621-1f79-45c8-bd89-c0c5ac11b2d8",
        "created_at": "2024-08-24T17:00",
        "products": [
            {
                "product_id": "3692d8f6-4e19-4ac4-add8-f06a8939164d",
                "quantity": 2
            }
        ]
    }
"""

class ProductOrderListCreateView(generics.ListCreateAPIView):
    queryset = ProductOrder.objects.all()
    serializer_class = ProductOrderSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    search_fields = ['id']
    filterset_class = ProductOrderFilter
    ordering_fields = ['is_urgent', 'created_at', 'due_date']
    pagination_class = ProductOrderPagination


class ProductOrderRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProductOrder.objects.all()
    serializer_class = ProductOrderSerializer
    lookup_field = "id"

class CustomerListCreateView(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class CustomerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    lookup_field = "id"
