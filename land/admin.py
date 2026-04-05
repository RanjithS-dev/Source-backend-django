from django.contrib import admin

from .models import Land, LandOwner


@admin.register(LandOwner)
class LandOwnerAdmin(admin.ModelAdmin):
    list_display = ("name", "phone_number", "village", "created_at")
    search_fields = ("name", "phone_number", "village")


@admin.register(Land)
class LandAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "village", "tree_count", "lease_start_date", "lease_end_date", "is_active")
    list_filter = ("village", "is_active")
    search_fields = ("name", "owner__name", "village")
