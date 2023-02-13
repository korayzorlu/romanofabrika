from django.contrib import admin

from .models import Status, Order

# Register your models here.

@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ["id", "title"]
    class Meta:
        model = Status
        
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["order_id", "order_date", "customer_name", "products"]
    list_display_links = ["customer_name"]
    search_fields = ["customer_name"]
    list_filter = ["order_date"]
    ordering = ["-order_date"]
    class Meta:
        model = Order