from django.contrib import admin

from .models import Vehicle, VehicleUsageLog


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ("registration_number", "vehicle_type", "capacity", "driver_name", "is_active")
    list_filter = ("vehicle_type", "is_active")
    search_fields = ("registration_number", "driver_name", "driver_phone")


@admin.register(VehicleUsageLog)
class VehicleUsageLogAdmin(admin.ModelAdmin):
    list_display = ("vehicle", "usage_date", "source", "destination", "fuel_cost")
    list_filter = ("usage_date",)
    search_fields = ("vehicle__registration_number", "source", "destination")
