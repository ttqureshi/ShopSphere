from django.contrib import admin
from django.http import HttpResponse
import csv

from .models import Order, OrderItem, Cart, CartItem

class ExportCsvMixin:
    def export_as_csv(self, request, queryset):
        order_field_names = ['id', 'user', 'order_date', 'total_price', 'full_name', 'contact_no', 'address', 'city', 'state', 'zipcode', 'country']
        order_item_field_names = ['product', 'quantity', 'total_price']

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=orders_with_items.csv'
        writer = csv.writer(response)

        header = order_field_names + ['orderitem_' + field for field in order_item_field_names]
        writer.writerow(header)

        for order in queryset:
            order_data = [getattr(order, field) for field in order_field_names]

            order_items = order.orderitem_set.all()

            if order_items.exists():
                for item in order_items:
                    order_item_data = [getattr(item, field) for field in order_item_field_names]
                    writer.writerow(order_data + order_item_data)
            else:
                writer.writerow(order_data + [''] * len(order_item_field_names))
            writer.writerow(["----------"])
        return response

    export_as_csv.short_description = "Export selected orders with items to CSV"

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin, ExportCsvMixin):
    actions = ["export_as_csv"]

admin.site.register(OrderItem)
admin.site.register(Cart)
admin.site.register(CartItem)
