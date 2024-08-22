from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework import status,generics
from rest_framework.response import Response

from .filters import ProductOrderFilter
from .models import Product, ProductOrder, ProductOrderProduct, Customer
from .serializers import (
    ProductSerializer,
    ProductOrderSerializer,
    ProductOrderProductSerializer,
    CustomerSerializer,
)

class ProductOrderPagination(PageNumberPagination):
    page_size = "10"

class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "id"

class ProductOrderListCreateView(generics.ListCreateAPIView):
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
            "is_urgent": false,
            "due_date": null,
            "status": null,
            "customer": null,
            "sale_staff": null,
            "logistic_staff": null,
            "deliverer": null,
            "created_at": null,
            "products": [{
                "product": {
                    "id": "b516c4f1-7be0-4372-848c-9fb08c858a7d",
                    "name": "Test Bon Xitec",
                    "category": "Cơ Khí Ô Tô",
                    "quantity": 7,
                    "price": 5
                }
            }]
        }
    """
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
