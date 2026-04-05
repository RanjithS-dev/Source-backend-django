from rest_framework import serializers

from .models import Vehicle, VehicleUsageLog


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = [
            "id",
            "registration_number",
            "vehicle_type",
            "capacity",
            "driver_name",
            "driver_phone",
            "is_active",
            "notes",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class VehicleUsageLogSerializer(serializers.ModelSerializer):
    vehicle_id = serializers.PrimaryKeyRelatedField(source="vehicle", queryset=Vehicle.objects.all(), write_only=True)
    vehicle = VehicleSerializer(read_only=True)

    class Meta:
        model = VehicleUsageLog
        fields = [
            "id",
            "vehicle",
            "vehicle_id",
            "usage_date",
            "source",
            "destination",
            "start_odometer",
            "end_odometer",
            "fuel_cost",
            "notes",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
