from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status,generics
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

from .filters import ProductFilter
from .models import Product, ProductOrder, ProductOrderProduct, Customer
from .serializers import (
    ProductSerializer,
    ProductOrderSerializer,
    ProductOrderProductSerializer,
    CustomerSerializer,
)

class ProductPagination(PageNumberPagination):
    page_size = '10'

class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['name']
    filterset_class = ProductFilter
    ordering_fields = ['name', 'quantity', 'price']
    pagination_class = ProductPagination
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
                "category": "Phuy",
                "quantity": 2,
                "price": 1
            },
            {
                "id": "f1d30788-7c2e-45d1-b033-ef734c54d98a",
                "name": "Test Phuy 3",
                "category": "Phuy",
                "quantity": 2,
                "price": 1
            },
            {
                "id": "8cd1f3bc-bd2e-4fbc-963f-2f4b0e2b35de",
                "name": "Test Phuy 1",
                "category": "Phuy",
                "quantity": 5,
                "price": 5
            }
        ]
    }
    POST: 
    {
        "name": "",
        "category": null,
        "quantity": null,
        "price": null
    }
    """

class ProductRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "id"

class ProductOrderListCreateView(generics.ListCreateAPIView):
    queryset = ProductOrder.objects.all()
    serializer_class = ProductOrderSerializer

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
