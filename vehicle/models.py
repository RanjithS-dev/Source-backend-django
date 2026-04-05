from django.db import models

from common.models import BaseModel


class Vehicle(BaseModel):
    registration_number = models.CharField(max_length=40, unique=True)
    vehicle_type = models.CharField(max_length=80, db_index=True)
    capacity = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    driver_name = models.CharField(max_length=180, blank=True)
    driver_phone = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True, db_index=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["registration_number"]

    def __str__(self) -> str:
        return self.registration_number


class VehicleUsageLog(BaseModel):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name="usage_logs")
    usage_date = models.DateField(db_index=True)
    source = models.CharField(max_length=180, blank=True)
    destination = models.CharField(max_length=180, blank=True)
    start_odometer = models.DecimalField(max_digits=10, decimal_places=1, null=True, blank=True)
    end_odometer = models.DecimalField(max_digits=10, decimal_places=1, null=True, blank=True)
    fuel_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-usage_date", "-created_at"]
        indexes = [
            models.Index(fields=["usage_date", "vehicle"]),
        ]

    def __str__(self) -> str:
        return f"{self.vehicle.registration_number} @ {self.usage_date}"
