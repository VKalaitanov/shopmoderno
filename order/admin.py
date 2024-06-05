from django.contrib import admin

from order.models import OrderItem, Order


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    readonly_fields = ('order', 'product', 'quantity', 'size', 'price')
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'created_timestamp', 'is_paid']
    list_filter = ['is_paid', 'created_timestamp']
    search_fields = ['user__username']
    readonly_fields = ('id', 'user', 'created_timestamp')
    inlines = [OrderItemInline]


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'size', 'price', 'get_cost']
    list_filter = ['order__created_timestamp', 'product__category']
    search_fields = ['order__user__username', 'product__name']
    readonly_fields = ('order', 'product', 'quantity', 'size', 'price', 'get_cost')

    def get_cost(self, obj):
        return obj.get_cost()

    get_cost.short_description = 'Total Cost'
