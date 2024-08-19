from rest_framework import status,generics
from rest_framework.response import Response
from .models import Product, ProductOrder, ProductOrderProduct, Customer
from .serializers import (
    ProductSerializer,
    ProductOrderSerializer,
    ProductOrderProductSerializer,
    CustomerSerializer,
)

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

    def get(self, request, *args, **kwargs):
        status_filter = request.query_params.get('status')

        if status_filter in ['Completed', 'Cancelled']:
            queryset = self.filter_queryset(self.get_queryset().filter(status__in = ['Completed', 'Cancelled']))
        else:
            queryset = self.get_queryset()

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class ProductOrderRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProductOrder.objects.all()
    serializer_class = ProductOrderSerializer
    lookup_field = "id"

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.status in ['Cancelled', 'Completed']:
            queryset = ProductOrder.objects.all().filter(status__in=['Cancelled', 'Completed'])
            serializer = ProductOrderSerializer(queryset, many=True)
            return Response(serializer.data)
        serializer = ProductOrderSerializer(instance)
        return Response(serializer.data)


class CustomerListCreateView(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class CustomerDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    lookup_field = "id"
