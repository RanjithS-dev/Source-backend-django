from django.contrib import admin

from .models import Buyer, SalesEntry


@admin.register(Buyer)
class BuyerAdmin(admin.ModelAdmin):
    list_display = ("name", "phone_number", "village")
    search_fields = ("name", "phone_number", "village")


@admin.register(SalesEntry)
class SalesEntryAdmin(admin.ModelAdmin):
    list_display = ("buyer", "land", "sale_date", "quantity", "unit_price", "transport_cost")
    list_filter = ("sale_date", "buyer")
    search_fields = ("buyer__name", "land__name", "notes")
