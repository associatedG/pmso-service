from rest_framework import serializers
from .models import ProductOrder, ProductOrderProduct, Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "category",
            "quantity",
            "price",
        ]


class ProductOrderProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=True)

    class Meta:
        model = ProductOrderProduct
        fields = [
            "id",
            "product",
            "product_order",
            "quantity",
        ]

class ProductOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductOrder
        fields = [
            "id",
            "is_urgent",
            "due_date",
            "status",
        ]

    def create(self, validated_data):
        return ProductOrder.objects.create(**validated_data)
