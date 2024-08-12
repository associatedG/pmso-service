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
    products = ProductSerializer(read_only=True)

    class Meta:
        model = ProductOrderProduct
        fields = [
            "id",
            "product_orders",
            "products",
            "quantity",
        ]


class ProductOrderSerializer(serializers.ModelSerializer):
    products = ProductOrderProductSerializer(many=True, read_only=True)

    class Meta:
        model = ProductOrder
        fields = [
            "id",
            "is_urgent",
            "due_date",
            "status",
            "products",
            "created_at",
            "last_modified",
            "sale_staff_id",
            "logistic_staff_id",
            "deliverer_id",
        ]

    def create(self, validated_data):
        products_data = validated_data.pop('products')
        product_order = ProductOrder.objects.create(**validated_data)
        for product_data in products_data:
            ProductOrderProduct.objects.create(product_order=product_order, **product_data)
        return product_order