from django.db import models

from common.models import BaseModel
from common.permissions import ROLE_ADMIN, ROLE_SUPERVISOR, ROLE_WORKER


class Employee(BaseModel):
    ROLE_CHOICES = [
        (ROLE_ADMIN, "Admin"),
        (ROLE_SUPERVISOR, "Supervisor"),
        (ROLE_WORKER, "Worker"),
    ]

    employee_code = models.CharField(max_length=40, unique=True)
    full_name = models.CharField(max_length=180, db_index=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_WORKER, db_index=True)
    department = models.CharField(max_length=120, db_index=True)
    designation = models.CharField(max_length=120, blank=True)
    phone_number = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    daily_wage = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    joined_on = models.DateField()
    is_active = models.BooleanField(default=True, db_index=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["full_name"]
        indexes = [
            models.Index(fields=["department", "role"]),
            models.Index(fields=["employee_code", "is_active"]),
        ]

    def __str__(self) -> str:
        return f"{self.employee_code} - {self.full_name}"
