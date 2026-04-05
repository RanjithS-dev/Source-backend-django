from datetime import date

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .services import build_dashboard_summary, get_employee_work_report, get_land_production_report, get_profit_loss_report


def _parse_date(value: str | None) -> date | None:
    if not value:
        return None
    return date.fromisoformat(value)


class DashboardSummaryAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        target_date = _parse_date(request.query_params.get("date"))
        return Response(build_dashboard_summary(target_date))


class LandProductionReportAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        date_from = _parse_date(request.query_params.get("date_from"))
        date_to = _parse_date(request.query_params.get("date_to"))
        return Response(get_land_production_report(date_from, date_to))


class EmployeeWorkReportAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        date_from = _parse_date(request.query_params.get("date_from"))
        date_to = _parse_date(request.query_params.get("date_to"))
        return Response(get_employee_work_report(date_from, date_to))


class ProfitLossReportAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        date_from = _parse_date(request.query_params.get("date_from"))
        date_to = _parse_date(request.query_params.get("date_to"))
        return Response(get_profit_loss_report(date_from, date_to))
