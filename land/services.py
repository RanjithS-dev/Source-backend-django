from .models import Land


def get_active_land_count() -> int:
    return Land.objects.filter(is_active=True).count()
