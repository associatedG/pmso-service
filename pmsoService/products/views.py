from rest_framework import generics,serializers
from .models import Product, ProductOrder, ProductOrderProduct
from .serializers import ProductSerializer, ProductOrderSerializer, ProductOrderProductSerializer


class ProductListCreatedView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductOrderListCreatedView(generics.ListCreateAPIView):
    queryset = ProductOrder.objects.all()
    serializer_class = ProductOrderSerializer

class ProductOrderRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProductOrder.objects.all()
    serializer_class = ProductOrderSerializer
    lookup_field = "id"


class ProductOrderProductListCreatedView(generics.ListCreateAPIView):
    queryset = ProductOrderProduct.objects.all()
    serializer_class = ProductOrderProductSerializer


class ProductOrderProductRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProductOrderProduct.objects.all()
    serializer_class = ProductOrderProductSerializer

