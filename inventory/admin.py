from django.contrib import admin
from .models import Store, GRN


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ["name", "location", "current_coconuts", "current_bags", "is_active", "created_at"]
    list_filter = ["is_active"]
    search_fields = ["name", "location"]


@admin.register(GRN)
class GRNAdmin(admin.ModelAdmin):
    list_display = ["store", "receipt_date", "coconut_count", "bag_count", "vehicle", "created_at"]
    list_filter = ["receipt_date", "store"]
    search_fields = ["store__name", "notes"]
    raw_id_fields = ["store", "worklog", "vehicle"]
