from django.db import models

from common.models import BaseModel
from employee.models import Employee
from land.models import Land
from vehicle.models import Vehicle
from worklog.models import WorkLog


class Expense(BaseModel):
    EXPENSE_TYPES = [
        ("wage", "Wage"),
        ("transport", "Transport"),
        ("fuel", "Fuel"),
        ("lease", "Lease"),
        ("maintenance", "Maintenance"),
        ("other", "Other"),
    ]

    expense_date = models.DateField(db_index=True)
    expense_type = models.CharField(max_length=30, choices=EXPENSE_TYPES, db_index=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    land = models.ForeignKey(Land, on_delete=models.SET_NULL, null=True, blank=True, related_name="expenses")
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True, related_name="expenses")
    vehicle = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, null=True, blank=True, related_name="expenses")
    worklog = models.ForeignKey(WorkLog, on_delete=models.SET_NULL, null=True, blank=True, related_name="expenses")
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-expense_date", "-created_at"]
        indexes = [
            models.Index(fields=["expense_date", "expense_type"]),
        ]

    def __str__(self) -> str:
        return f"{self.expense_type} @ {self.expense_date}"
