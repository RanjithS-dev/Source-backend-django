from rest_framework import serializers

from .models import Land, LandOwner


class LandOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = LandOwner
        fields = ["id", "name", "phone_number", "village", "address", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]


class LandSerializer(serializers.ModelSerializer):
    owner_id = serializers.PrimaryKeyRelatedField(source="owner", queryset=LandOwner.objects.all(), write_only=True)
    owner = LandOwnerSerializer(read_only=True)

    class Meta:
        model = Land
        fields = [
            "id",
            "owner",
            "owner_id",
            "name",
            "village",
            "area_acres",
            "lease_start_date",
            "lease_end_date",
            "lease_amount",
            "tree_count",
            "lease_notes",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
