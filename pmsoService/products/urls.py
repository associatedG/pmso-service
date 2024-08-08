from django.urls import path
from .views import ProductOrderCreateAPIView

urlpatterns = [
		path(
			"",
			ProductOrderCreateAPIView.as_view(),
			name="product_order_create"
		)
]
