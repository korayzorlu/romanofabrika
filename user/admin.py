from django.contrib import admin

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import Employee, UserCategory, StaffCategory

# Register your models here.

@admin.register(Employee)
class EmployeeUser(admin.ModelAdmin):
    list_display = ["image", "user"]
    search_fields = ["image", "user__username"]
    class Meta:
        model = Employee

@admin.register(UserCategory)
class UserCategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "title"]
    class Meta:
        model = UserCategory

@admin.register(StaffCategory)
class StaffCategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "title"]
    class Meta:
        model = StaffCategory       

# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class EmployeeInline(admin.StackedInline):
    model = Employee
    can_delete = False
    verbose_name_plural = 'employee'

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (EmployeeInline,)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
