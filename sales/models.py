from django.db import models

from common.models import BaseModel
from land.models import Land
from worklog.models import WorkLog


class Buyer(BaseModel):
    name = models.CharField(max_length=180, db_index=True)
    phone_number = models.CharField(max_length=30, blank=True)
    village = models.CharField(max_length=120, blank=True, db_index=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name


class SalesEntry(BaseModel):
    buyer = models.ForeignKey(Buyer, on_delete=models.PROTECT, related_name="sales_entries")
    land = models.ForeignKey(Land, on_delete=models.SET_NULL, null=True, blank=True, related_name="sales_entries")
    worklog = models.ForeignKey(WorkLog, on_delete=models.SET_NULL, null=True, blank=True, related_name="sales_entries")
    sale_date = models.DateField(db_index=True)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    transport_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-sale_date", "-created_at"]
        indexes = [
            models.Index(fields=["sale_date", "buyer"]),
        ]

    def __str__(self) -> str:
        return f"{self.buyer.name} @ {self.sale_date}"
