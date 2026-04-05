from .models import Employee


def get_active_worker_count() -> int:
    return Employee.objects.filter(is_active=True).count()
