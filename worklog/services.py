from employee.models import Employee

from .models import WorkLog, WorkLogAssignment


def sync_worklog_assignments(worklog: WorkLog, worker_ids: list[int]) -> None:
    """Replace worker assignments for a worklog using plain employee ids."""

    valid_ids = list(Employee.objects.filter(id__in=worker_ids).values_list("id", flat=True))
    WorkLogAssignment.objects.filter(worklog=worklog).exclude(employee_id__in=valid_ids).delete()

    existing_ids = set(
        WorkLogAssignment.objects.filter(worklog=worklog, employee_id__in=valid_ids).values_list("employee_id", flat=True)
    )
    WorkLogAssignment.objects.bulk_create(
        [
            WorkLogAssignment(worklog=worklog, employee_id=employee_id)
            for employee_id in valid_ids
            if employee_id not in existing_ids
        ]
    )
