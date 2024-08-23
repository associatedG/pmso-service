from rest_framework.pagination import PageNumberPagination


class ProductOrderPagination(PageNumberPagination):
    page_size = "10"


class ProductPagination(PageNumberPagination):
    page_size = "10"


class CustomerPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100
