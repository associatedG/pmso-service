from rest_framework import generics
from .models import Product, ProductOrder, ProductOrderProduct


class ProductOrderCreateAPIView(generics.CreateAPIView):
	queryset = ProductOrder.objects.all()
	serializer_class = ProductOrderProductSerializer

