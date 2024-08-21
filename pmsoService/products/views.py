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
    queryset = ProductOrder.objects.all()
    serializer_class = ProductOrderSerializer
    filter_backends = [DjangoFilterBackend]
    search_fields = ['id']
    filterset_class = ProductOrderFilter
    ordering_fields = ['price', 'is_urgent', 'created_at', 'due_date']
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
