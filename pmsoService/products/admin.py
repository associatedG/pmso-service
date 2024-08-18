from django.contrib import admin
from .models import Product, ProductOrder, ProductOrderProduct, Customer


class ProductOrderProductInline(admin.TabularInline):
    model = ProductOrderProduct
    extra = 1  # Number of extra forms to display
    verbose_name = "Product"
    verbose_name_plural = "Products"


class ProductOrderAdmin(admin.ModelAdmin):
    inlines = [ProductOrderProductInline]


admin.site.register(Product)
admin.site.register(ProductOrder, ProductOrderAdmin)
admin.site.register(ProductOrderProduct)
admin.site.register(Customer)
