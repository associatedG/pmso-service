from django.contrib import admin
from .models import Product, ProductOrder, ProductOrderProduct, Customer
from simple_history.admin import SimpleHistoryAdmin


class ProductOrderProductInline(admin.TabularInline):
    model = ProductOrderProduct
    extra = 1  # Number of extra forms to display
    verbose_name = "Product"
    verbose_name_plural = "Products"


class ProductOrderAdmin(SimpleHistoryAdmin, admin.ModelAdmin):
    inlines = [ProductOrderProductInline]


admin.site.register(Product, SimpleHistoryAdmin)
admin.site.register(ProductOrder, ProductOrderAdmin)
admin.site.register(ProductOrderProduct, SimpleHistoryAdmin)
admin.site.register(Customer, SimpleHistoryAdmin)
