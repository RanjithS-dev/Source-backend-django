from django.db import models


class BaseModel(models.Model):
    """Shared audit fields for all business-domain records."""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
