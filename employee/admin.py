from django.contrib import admin

from .models import Employee


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("employee_code", "full_name", "role", "department", "daily_wage", "is_active")
    list_filter = ("role", "department", "is_active")
    search_fields = ("employee_code", "full_name", "phone_number", "email")
