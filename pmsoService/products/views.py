from rest_framework import generics
from .models import Product, ProductOrder, ProductOrderProduct
from .serializers import ProductSerializer, ProductOrderSerializer, ProductOrderProductSerializer

# Product View
class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

# ProductOrder View
class ProductOrderListCreateView(generics.ListCreateAPIView):
    queryset = ProductOrder.objects.all()
    serializer_class = ProductOrderSerializer


class ProductOrderRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProductOrder.objects.all()
    serializer_class = ProductOrderSerializer


# ProductOrderProduct Views
class ProductOrderProductListCreateView(generics.ListCreateAPIView):
    queryset = ProductOrderProduct.objects.all()
    serializer_class = ProductOrderProductSerializer


class ProductOrderProductRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProductOrderProduct.objects.all()
    serializer_class = ProductOrderProductSerializer
