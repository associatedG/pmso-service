from rest_framework import serializers
from .models import ProductOrder, ProductOrderProduct, Product, Customer
import re


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "is_active",
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
    customer_name = serializers.CharField(source="customer.name", read_only=True)

    class Meta:
        model = ProductOrder
        fields = [
            "id",
            "name",
            "is_urgent",
            "due_date",
            "status",
            "customer",
            "customer_name",
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


class CustomerSerializer(serializers.ModelSerializer):
    orders = ProductOrderSerializer(many=True, read_only=True)
    number_of_current_orders = serializers.SerializerMethodField()
    number_of_orders = serializers.SerializerMethodField()

    class Meta:
        model = Customer
        fields = [
            "id",
            "name",
            "phone",
            "tier",
            "fax",
            "email",
            "contact_list",
            "address",
            "note",
            "created_at",
            "modified_at",
            "orders",
            "number_of_current_orders",
            "number_of_orders",
        ]

    def get_number_of_orders(self, obj):
        return obj.orders.count()

    def get_number_of_current_orders(self, obj):
        return obj.orders.filter(
            status__in=["Open", "Planning Production", "In Production", "Delivering"]
        ).count()

    def validate_phone(self, value):
        pattern = r"^(0[35789])([0-9]{8})\b$"
        if not re.match(pattern, value):
            raise serializers.ValidationError(
                "Invalid phone number format. Expected format: 0[35789] followed by 8 digits."
            )
        return value
