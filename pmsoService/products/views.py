from rest_framework import generics,serializers
from .models import Product, ProductOrder, ProductOrderProduct
from .serializers import ProductSerializer, ProductOrderSerializer, ProductOrderProductSerializer


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

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProductOrderRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProductOrder.objects.all()
    serializer_class = ProductOrderSerializer


class ProductOrderProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all(),
    serializer_class = ProductOrderSerializer

    def create(self, request, *args, **kwargs):
        product_order_id = request.data.get('product_order')
        product_id = request.data.get('product')
        quantity = request.data.get('quantity')

        # Create ProductOrderProduct entry
        product_order = ProductOrder.objects.get(id=product_order_id)
        product = Product.objects.get(id=product_id)

        ProductOrderProduct.objects.create(
            product_order=product_order,
            product=product,
            quantity=quantity
        )

        return Response({"message": "Product added to order successfully"}, status=status.HTTP_201_CREATED)



class ProductOrderProductRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProductOrderProduct.objects.all()
    serializer_class = ProductOrderProductSerializer


