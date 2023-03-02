from django.contrib import admin

# Register your models here.

from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["title", "parent",]
    class Meta:
        model = Category

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["product_id", "title"]
    list_display_links = ["title"]
    search_fields = ["title"]
    list_filter = ["title"]
    ordering = ["-title"]
    class Meta:
        model = Product