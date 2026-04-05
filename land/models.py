from django.db import models

from common.models import BaseModel


class LandOwner(BaseModel):
    name = models.CharField(max_length=180, db_index=True)
    phone_number = models.CharField(max_length=30, blank=True)
    village = models.CharField(max_length=120, blank=True, db_index=True)
    address = models.TextField(blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class Land(BaseModel):
    owner = models.ForeignKey(LandOwner, on_delete=models.PROTECT, related_name="lands")
    name = models.CharField(max_length=180, db_index=True)
    village = models.CharField(max_length=120, db_index=True)
    area_acres = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    lease_start_date = models.DateField()
    lease_end_date = models.DateField()
    lease_amount = models.DecimalField(max_digits=12, decimal_places=2)
    tree_count = models.PositiveIntegerField(default=0)
    lease_notes = models.TextField(blank=True)
    is_active = models.BooleanField(default=True, db_index=True)

    class Meta:
        ordering = ["name"]
        indexes = [
            models.Index(fields=["village", "is_active"]),
            models.Index(fields=["lease_start_date", "lease_end_date"]),
        ]

    def __str__(self) -> str:
        return self.name
