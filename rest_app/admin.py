from django.contrib import admin
from .models import Dish

@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')

from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'client', 'total_price', 'status', 'created')
    list_filter = ('status', 'created')
    search_fields = ('full_name', 'phone', 'address', 'items')
    readonly_fields = ('created',)