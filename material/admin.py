from django.contrib import admin

from .models import Source, Material, Category, Unit

# Register your models here.

@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "slug"]
    class Meta:
        model = Source
        
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "title"]
    class Meta:
        model = Category
        
@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ["id", "title"]
    class Meta:
        model = Unit
               
@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ["id", "category", "title", "unit"]
    ordering = ["title"]
    class Meta:
        model = Material