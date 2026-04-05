from datetime import date
from decimal import Decimal

from django.db.models import Count, DecimalField, ExpressionWrapper, F, Q, Sum
from django.db.models.functions import Coalesce, TruncMonth

from employee.models import Employee
from expenses.models import Expense
from land.models import Land
from sales.models import SalesEntry
from worklog.models import WorkLog, WorkLogAssignment


def _resolve_range(date_from: date | None, date_to: date | None) -> tuple[date | None, date | None]:
    if date_from and date_to and date_from > date_to:
        return date_to, date_from
    return date_from, date_to


def build_dashboard_summary(target_date: date | None = None) -> dict:
    target_date = target_date or date.today()
    revenue_expression = ExpressionWrapper(
        F("quantity") * F("unit_price"),
        output_field=DecimalField(max_digits=14, decimal_places=2),
    )

    daily_harvest = (
        WorkLog.objects.filter(work_date=target_date).aggregate(
            total=Coalesce(Sum("coconut_count"), 0)
        )["total"]
    )
    total_revenue = (
        SalesEntry.objects.aggregate(total=Coalesce(Sum(revenue_expression), Decimal("0.00")))["total"]
    )

    return {
        "totalLands": Land.objects.filter(is_active=True).count(),
        "activeWorkers": Employee.objects.filter(is_active=True).count(),
        "dailyHarvest": daily_harvest,
        "totalRevenue": float(total_revenue),
    }


def get_land_production_report(date_from: date | None = None, date_to: date | None = None) -> list[dict]:
    date_from, date_to = _resolve_range(date_from, date_to)
    filters = Q()
    if date_from:
        filters &= Q(worklogs__work_date__gte=date_from)
    if date_to:
        filters &= Q(worklogs__work_date__lte=date_to)

    items = (
        Land.objects.select_related("owner")
        .annotate(
            total_coconuts=Coalesce(Sum("worklogs__coconut_count", filter=filters), 0),
            total_worklogs=Count("worklogs", filter=filters, distinct=True),
        )
        .order_by("-total_coconuts", "name")
    )

    return [
        {
            "id": land.id,
            "name": land.name,
            "village": land.village,
            "ownerName": land.owner.name,
            "treeCount": land.tree_count,
            "totalCoconuts": land.total_coconuts,
            "totalWorkLogs": land.total_worklogs,
        }
        for land in items
    ]


def get_employee_work_report(date_from: date | None = None, date_to: date | None = None) -> list[dict]:
    date_from, date_to = _resolve_range(date_from, date_to)
    filters = Q(worklog_assignments__isnull=False)
    if date_from:
        filters &= Q(worklog_assignments__worklog__work_date__gte=date_from)
    if date_to:
        filters &= Q(worklog_assignments__worklog__work_date__lte=date_to)

    assignments = (
        Employee.objects.annotate(
            total_assignments=Count("worklog_assignments", filter=filters, distinct=True),
            total_units=Coalesce(Sum("worklog_assignments__units_completed", filter=filters), 0),
            total_coconuts=Coalesce(
                Sum("worklog_assignments__worklog__coconut_count", filter=filters),
                0,
            ),
        )
        .filter(total_assignments__gt=0)
        .order_by("-total_assignments", "full_name")
    )

    return [
        {
            "id": employee.id,
            "employeeCode": employee.employee_code,
            "name": employee.full_name,
            "role": employee.role,
            "department": employee.department,
            "assignmentCount": employee.total_assignments,
            "unitsCompleted": employee.total_units,
            "workLogCoconuts": employee.total_coconuts,
        }
        for employee in assignments
    ]


def get_profit_loss_report(date_from: date | None = None, date_to: date | None = None) -> dict:
    date_from, date_to = _resolve_range(date_from, date_to)
    revenue_expression = ExpressionWrapper(
        F("quantity") * F("unit_price"),
        output_field=DecimalField(max_digits=14, decimal_places=2),
    )

    revenue_filters = Q()
    expense_filters = Q()
    if date_from:
        revenue_filters &= Q(sale_date__gte=date_from)
        expense_filters &= Q(expense_date__gte=date_from)
    if date_to:
        revenue_filters &= Q(sale_date__lte=date_to)
        expense_filters &= Q(expense_date__lte=date_to)

    total_revenue = SalesEntry.objects.filter(revenue_filters).aggregate(
        total=Coalesce(Sum(revenue_expression), Decimal("0.00"))
    )["total"]
    total_expenses = Expense.objects.filter(expense_filters).aggregate(
        total=Coalesce(Sum("amount"), Decimal("0.00"))
    )["total"]

    monthly_revenue = (
        SalesEntry.objects.filter(revenue_filters)
        .annotate(period=TruncMonth("sale_date"))
        .values("period")
        .annotate(total=Coalesce(Sum(revenue_expression), Decimal("0.00")))
        .order_by("period")
    )
    monthly_expenses = {
        item["period"]: item["total"]
        for item in Expense.objects.filter(expense_filters)
        .annotate(period=TruncMonth("expense_date"))
        .values("period")
        .annotate(total=Coalesce(Sum("amount"), Decimal("0.00")))
        .order_by("period")
    }

    monthly_breakdown = []
    for item in monthly_revenue:
        period = item["period"]
        expense_total = monthly_expenses.get(period, Decimal("0.00"))
        monthly_breakdown.append(
            {
                "period": period.isoformat() if period else None,
                "revenue": float(item["total"]),
                "expenses": float(expense_total),
                "profit": float(item["total"] - expense_total),
            }
        )

    return {
        "totalRevenue": float(total_revenue),
        "totalExpenses": float(total_expenses),
        "totalProfit": float(total_revenue - total_expenses),
        "monthlyBreakdown": monthly_breakdown,
    }
