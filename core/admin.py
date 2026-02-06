from django.contrib import admin
from .models import Customer, Product, Round, Order, OrderItem

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "active")
    search_fields = ("name", "phone")
    list_filter = ("active",)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "unit", "sell_price", "buy_price", "active")
    search_fields = ("name", "unit")
    list_filter = ("active",)

@admin.register(Round)
class RoundAdmin(admin.ModelAdmin):
    list_display = ("date", "travel_km", "is_active")
    list_filter = ("is_active",)
    ordering = ("-is_active", "-date")

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("customer", "round", "source", "paid", "picked_up", "created_at")
    list_filter = ("paid", "picked_up", "source", "round")
    search_fields = ("customer__name",)
    inlines = [OrderItemInline]
