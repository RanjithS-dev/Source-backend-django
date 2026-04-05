from django.contrib import admin

from .models import Expense


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ("expense_date", "expense_type", "amount", "land", "employee", "vehicle")
    list_filter = ("expense_type", "expense_date")
    search_fields = ("notes", "land__name", "employee__full_name", "vehicle__registration_number")
