from django_filters.rest_framework import FilterSet, CharFilter
from products.models import ProductOrder, Product, Customer


class ProductOrderFilter(FilterSet):
    status = CharFilter(method="filter_status")

    def filter_status(self, queryset, name, value):
        status_list = value.split(",")
        return queryset.filter(status__in=status_list)

    class Meta:
        model = ProductOrder

        fields = {
            "is_urgent": ["exact"],
            "due_date": ["gte", "lte", "exact"],
            "status": ["exact"],
        }


class ProductFilter(FilterSet):
    class Meta:
        model = Product

        fields = {
            "category": ["exact"],
            "is_active": ["exact"],
        }


class CustomerFilter(FilterSet):
    class Meta:
        model = Customer

        fields = {
            "tier": ["exact"],
        }
