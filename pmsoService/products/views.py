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
