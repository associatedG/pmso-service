from rest_framework import generics
from .models import Product, ProductOrder, ProductOrderProduct
from .serializers import ProductSerializer, ProductOrderProductSerializer, ProductOrderSerializer


class ProductOrderCreateAPIView(generics.CreateAPIView):
	queryset = ProductOrder.objects.all()
	serializer_class = ProductOrderProductSerializer

