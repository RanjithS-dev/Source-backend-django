from rest_framework import serializers

from land.models import Land
from land.serializers import LandSerializer
from worklog.models import WorkLog
from worklog.serializers import WorkLogSerializer

from .models import Buyer, SalesEntry


class BuyerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Buyer
        fields = ["id", "name", "phone_number", "village", "notes", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]


class SalesEntrySerializer(serializers.ModelSerializer):
    buyer_id = serializers.PrimaryKeyRelatedField(source="buyer", queryset=Buyer.objects.all(), write_only=True)
    land_id = serializers.PrimaryKeyRelatedField(
        source="land",
        queryset=Land.objects.all(),
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
    buyer = BuyerSerializer(read_only=True)
    land = LandSerializer(read_only=True)
    worklog = WorkLogSerializer(read_only=True)
    gross_amount = serializers.SerializerMethodField()

    class Meta:
        model = SalesEntry
        fields = [
            "id",
            "buyer",
            "buyer_id",
            "land",
            "land_id",
            "worklog",
            "worklog_id",
            "sale_date",
            "quantity",
            "unit_price",
            "transport_cost",
            "gross_amount",
            "notes",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "gross_amount"]

    def get_gross_amount(self, obj):
        return float(obj.quantity * obj.unit_price)
