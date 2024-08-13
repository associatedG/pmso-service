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
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        write_only=True, source="product", queryset=Product.objects.all()
    )

    class Meta:
        model = ProductOrderProduct
        fields = ["product", "product_id", "quantity"]

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than zero.")
        return value


class ProductOrderSerializer(serializers.ModelSerializer):
    products = ProductOrderProductSerializer(many=True)

    class Meta:
        model = ProductOrder
        fields = [
            "id",
            "is_urgent",
            "due_date",
            "status",
            "sale_staff",
            "logistic_staff",
            "deliverer",
            "last_modified",
            "created_at",
            "products",
        ]

    def create(self, validated_data):
        products_data = validated_data.pop("products")
        product_order = ProductOrder.objects.create(**validated_data)
        for product_data in products_data:
            ProductOrderProduct.objects.create(
                product_order=product_order, **product_data
            )
        return product_order
