from rest_framework import serializers

from employee.models import Employee
from employee.serializers import EmployeeSerializer
from land.models import Land
from land.serializers import LandSerializer
from vehicle.models import Vehicle
from vehicle.serializers import VehicleSerializer
from worklog.models import WorkLog
from worklog.serializers import WorkLogSerializer

from .models import Expense


class ExpenseSerializer(serializers.ModelSerializer):
    land_id = serializers.PrimaryKeyRelatedField(
        source="land",
        queryset=Land.objects.all(),
        write_only=True,
        required=False,
        allow_null=True,
    )
    employee_id = serializers.PrimaryKeyRelatedField(
        source="employee",
        queryset=Employee.objects.all(),
        write_only=True,
        required=False,
        allow_null=True,
    )
    vehicle_id = serializers.PrimaryKeyRelatedField(
        source="vehicle",
        queryset=Vehicle.objects.all(),
        write_only=True,
        required=False,
        allow_null=True,
    )
    worklog_id = serializers.PrimaryKeyRelatedField(
        source="worklog",
        queryset=WorkLog.objects.all(),
        write_only=True,
        required=False,
        allow_null=True,
    )
    land = LandSerializer(read_only=True)
    employee = EmployeeSerializer(read_only=True)
    vehicle = VehicleSerializer(read_only=True)
    worklog = WorkLogSerializer(read_only=True)

    class Meta:
        model = Expense
        fields = [
            "id",
            "expense_date",
            "expense_type",
            "amount",
            "land",
            "land_id",
            "employee",
            "employee_id",
            "vehicle",
            "vehicle_id",
            "worklog",
            "worklog_id",
            "notes",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
