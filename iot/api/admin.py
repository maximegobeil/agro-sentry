from django.contrib import admin

from .models import SensorReading


@admin.register(SensorReading)
class SensorReadingAdmin(admin.ModelAdmin):
    list_display = ("id", "sensor_id", "timestamp", "get_metadata")
    list_filter = ("sensor_id", "timestamp")
    search_fields = ("sensor_id", "id")
    date_hierarchy = "timestamp"
    readonly_fields = ("id",)  # If id is auto-generated

    def get_metadata(self, obj):
        return obj.metadata

    get_metadata.short_description = "Metadata"
