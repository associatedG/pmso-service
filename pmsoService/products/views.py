from rest_framework import generics
from .models import Product, ProductOrder, ProductOrderProduct
from .serializers import ProductSerializer, ProductOrderSerializer, ProductOrderProductSerializer


# ProductOrder View
class ProductOrderListCreateView(generics.ListCreateAPIView):
    queryset = ProductOrder.objects.all()
    serializer_class = ProductOrderSerializer


class ProductOrderRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProductOrder.objects.all()
    serializer_class = ProductOrderSerializer


class ProductOrderProductListCreateView(generics.ListCreateAPIView):
    queryset = ProductOrder.objects.all()
    serializer_class = ProductOrderSerializer


class ProductOrderProductRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProductOrderProduct.objects.all()
    serializer_class = ProductOrderProductSerializer


