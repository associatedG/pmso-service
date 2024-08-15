from requests import Response
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

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        status_value = request.data.get("status")
        if status_value == ProductOrder.CANCELLED:
            if instance.status != ProductOrder.CANCELLED:
                instance.status = ProductOrder.CANCELLED
                instance.save()
                return Response({"status": "Cancelled"}, status=status.HTTP_200_OK)
            else:
                return Response({"status": "Product Order is already cancelled"}, status=status.HTTP_400_BAD_REQUEST)
        return super().partial_update(request, *args, **kwargs)

class CustomerListCreateView(generics.ListCreateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
