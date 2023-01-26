from django.contrib import admin

from .models import Source, Material

# Register your models here.

@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "slug"]
    class Meta:
        model = Source
        
@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ["title"]
    class Meta:
        model = Material