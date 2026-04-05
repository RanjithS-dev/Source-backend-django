from django.contrib import admin

from .models import WorkLog, WorkLogAssignment


class WorkLogAssignmentInline(admin.TabularInline):
    model = WorkLogAssignment
    extra = 0


@admin.register(WorkLog)
class WorkLogAdmin(admin.ModelAdmin):
    list_display = ("work_date", "land", "supervisor", "vehicle", "coconut_count", "bag_count")
    list_filter = ("work_date", "land")
    search_fields = ("land__name", "supervisor__full_name", "notes")
    inlines = [WorkLogAssignmentInline]
