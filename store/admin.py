from django.contrib import admin
from .models import Shoe, CartItem, Order, OrderItem

admin.site.register(Shoe)
admin.site.register(CartItem)

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'payment_method', 'status', 'created_at']
    inlines = [OrderItemInline]

admin.site.register(Order, OrderAdmin)
