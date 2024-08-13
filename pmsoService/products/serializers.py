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
    # product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    product = ProductSerializer(many=True)

    class Meta:
        model = ProductOrderProduct
        fields = [
            "id",
            "product",
            "product_order",
            "quantity",
        ]

    # def to_representation(self, instance):
    #     # Ensure correct access to product ID
    #     representation = super().to_representation(instance)
    #     # print(representation)
    #     representation['product'] = str(instance.product.id)
    #     return representation


class ProductOrderSerializer(serializers.ModelSerializer):
    # products = ProductOrderProductSerializer(many=True)

    class Meta:
        model = ProductOrder
        fields = [
            "id",
            "is_urgent",
            "due_date",
            "status",
            # "products",
            # "created_at",
            # "last_modified",
            # "sale_staff_id",
            # "logistic_staff_id",
            # "deliverer_id",
        ]

    def create(self, validated_data):
        return ProductOrder.objects.create(**validated_data)

    # def create(self, validated_data):
    #     print(validated_data)
    #     products_data = validated_data.pop('products')
    #     print(f"Products data: {products_data}")  # Log products_data
    #     product_order = ProductOrder.objects.create(**validated_data)
    #     for product_data in products_data:
    #         print(f"Product data: {product_data}")  # Log individual product data
    #         product = product_data.get('id')
    #         if not product:
    #             raise ValueError("Product ID is missing")
    #         print(product)
    #         ProductOrderProduct.objects.create(
    #             product_order=product_order,
    #             product=product,
    #             quantity=product_data['quantity']
    #         )
    #     return product_order