from django.contrib import admin

from .models import Company, Expense, Category, Unit

# Register your models here.


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ["id", "title"]
    class Meta:
        model = Company
        
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
               
@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ["created_date", "id", "category", "title", "unit"]
    list_display_links = ["title"]
    search_fields = ["title"]
    list_filter = ["created_date"]
    ordering = ["-created_date"]
    class Meta:
        model = Expense