from django.contrib import admin
from django.db.models import Sum
from .models import Order, ProductsInOrder

from django.contrib import admin
from .models import Order, ProductsInOrder, Product


class ProductsInOrderInline(admin.TabularInline):
    model = ProductsInOrder
    extra = 0
    readonly_fields = ('product', 'quantity', 'total_price', 'unit_price')
    fields = ('product', 'quantity', 'unit_price', 'total_price')

    def unit_price(self, instance):
        return instance.product.price

    unit_price.short_description = 'Цена за штуку'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    ordering = ('-created',)
    list_display = ('customer', 'quantity', 'total_price', 'created',)
    readonly_fields = ('customer', 'quantity', 'total_price', 'created',)

    inlines = (ProductsInOrderInline,)

    def quantity(self, obj):
        return ProductsInOrder.objects.filter(order=obj).count()

    quantity.short_description = 'Количество позиций'

    def total_price(self, obj):
        return ProductsInOrder.objects.filter(order=obj).aggregate(total=Sum('total_price'))['total'] or 0

    total_price.short_description = 'Итоговая цена заказа'

    def has_change_permission(self, request, obj=None):
        return True
