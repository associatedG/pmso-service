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
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = ProductOrderProduct
        fields = [
            "id",
            "product",
            "quantity",
        ]


class ProductOrderSerializer(serializers.ModelSerializer):
    products = ProductOrderProductSerializer(many=True)

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
        print(f"Validated data: {validated_data}")
        products_data = validated_data.pop('products')
        product_order = ProductOrder.objects.create(**validated_data)
        for product_data in products_data:
            print(f"Product data: {product_data}")
            # Retrieve the product instance by ID
            product = product_data["product"]
            ProductOrderProduct.objects.create(
                product_order=product_order,
                product=product_data["product"],
                quantity=product_data.get('quantity')
            )
        return product_order