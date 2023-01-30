from django.contrib import admin

from .models import Company, Expense, Category, Unit

# Register your models here.


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "slug"]
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
    list_display = ["id", "category", "title", "unit"]
    ordering = ["created_date"]
    class Meta:
        model = Expense