from django.contrib import admin
from .models import Order, OrderItem

# Register your models here.

class OrderAdmin(admin.ModelAdmin):
    list_display = ('user','store','total_amount','status','order_date')
    list_display_links = ('user','store')
    list_editable = ('status',)
    search_fields = ('user','store','status','order_date')
    list_per_page = 25


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order','product','quantity','price')
    list_display_links = ('order','product')
    list_editable = ('quantity',)
    search_fields = ('order','product')
    list_per_page = 25

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
