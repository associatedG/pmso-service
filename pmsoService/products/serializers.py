from rest_framework import serializers
from .models import ProductOrder, ProductOrderProduct, Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id',
                  'name',
                  'category',
                  'quantity',
                  'price']


class ProductOrderProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = ProductOrderProduct
        fields = ['id',
                  'product_orders',
                  'products',
                  'quantity']


class ProductOrderSerializer(serializers.ModelSerializer):
    products = ProductOrderProductSerializer(many=True, read_only=True)

    class Meta:
        model = ProductOrder
        fields = ['id',
                  'isUrgent',
                  'dueDate',
                  'status',
                  'products',
                  'createdAt',
                  'lastUpdated',
                  'lastModified']
