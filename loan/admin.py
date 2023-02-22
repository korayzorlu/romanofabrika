from django.contrib import admin

# Register your models here.

from .models import Bank, InstallmentStatus, LoanStatus

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