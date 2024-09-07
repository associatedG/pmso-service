from rest_framework import serializers
from .models import ProductOrder, ProductOrderProduct, Product, Customer
from account.serializers import UserSerializer
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


class CustomerSerializer(serializers.ModelSerializer):
    number_of_orders = serializers.IntegerField(read_only=True)
    number_of_current_orders = serializers.IntegerField(read_only=True)

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
            "number_of_orders",
            "number_of_current_orders",
        ]

    def validate_phone(self, value):
        pattern = r"^(0[35789])([0-9]{8})\b$"
        if not re.match(pattern, value):
            raise serializers.ValidationError(
                "Invalid phone number format. Expected format: 0[35789] followed by 8 digits."
            )
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

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.is_urgent = validated_data.get("is_urgent", instance.is_urgent)
        instance.due_date = validated_data.get("due_date", instance.due_date)
        instance.status = validated_data.get("status", instance.status)
        instance.customer = validated_data.get("customer", instance.customer)
        instance.sale_staff = validated_data.get("sale_staff", instance.sale_staff)
        instance.logistic_staff = validated_data.get(
            "logistic_staff", instance.logistic_staff
        )
        instance.deliverer = validated_data.get("deliverer", instance.deliverer)
        instance.save()

        products_data = validated_data.pop("products", None)
        if products_data:
            for product_data in products_data:
                product_instance = ProductOrderProduct.objects.get(
                    product_order=instance, product=product_data["product"]
                )
                product_instance.quantity = product_data["quantity"]
                product_instance.save()

        return instance


class GetProductOrderSerializer(serializers.ModelSerializer):
    products = ProductOrderProductSerializer(many=True)
    customer = CustomerSerializer(read_only=True)
    sale_staff = UserSerializer(read_only=True)
    logistic_staff = UserSerializer(read_only=True)
    deliverer = UserSerializer(read_only=True)

    class Meta:
        model = ProductOrder
        fields = [
            "id",
            "name",
            "is_urgent",
            "due_date",
            "status",
            "customer",
            "sale_staff",
            "logistic_staff",
            "deliverer",
            "last_modified",
            "created_at",
            "products",
        ]
