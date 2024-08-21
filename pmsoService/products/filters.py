from django_filters.rest_framework import FilterSet
from products.models import ProductOrder

class ProductOrderFilter(FilterSet):
	class Meta:
		model = ProductOrder

		fields = {
			'is_urgent': ['exact'],
			'due_date': ['gte', 'lte', 'exact'],
			'status': ['exact'],
		}