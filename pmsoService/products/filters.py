from django_filters.rest_framework import FilterSet
from products.models import Product

class ProductFilter(FilterSet):
	class Meta:
		model = Product

		fields = {
			"category": ["exact"],
			"is_active": ["exact"],
		}