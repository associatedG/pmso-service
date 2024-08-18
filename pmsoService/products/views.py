from rest_framework import status,generics
from rest_framework.response import Response
from .models import Product, ProductOrder, ProductOrderProduct, Customer
from .serializers import (
    ProductSerializer,
    ProductOrderSerializer,
    ProductOrderProductSerializer,
    CustomerSerializer,
)


# ProductOrder View
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
