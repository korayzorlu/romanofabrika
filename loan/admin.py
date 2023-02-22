from django.contrib import admin

# Register your models here.

from .models import Bank, InstallmentStatus, LoanStatus, Loan

@admin.register(Bank)
class BankAdmin(admin.ModelAdmin):
    list_display = ["id", "title"]
    class Meta:
        model = Bank
        
@admin.register(InstallmentStatus)
class InstallmentStatusAdmin(admin.ModelAdmin):
    list_display = ["id", "title"]
    class Meta:
        model = InstallmentStatus
        
@admin.register(LoanStatus)
class LoanStatusAdmin(admin.ModelAdmin):
    list_display = ["id", "title"]
    class Meta:
        model = LoanStatus
        
@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ["start_date", "id", "bank", "title"]
    list_display_links = ["title"]
    search_fields = ["title"]
    list_filter = ["start_date"]
    ordering = ["-start_date"]
    class Meta:
        model = Loan