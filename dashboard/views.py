from django.utils import timezone
from django.db.models import Sum, Q
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from decimal import Decimal

from invoices.models import Invoice, InvoiceStatus
from quotes.models import Quote, QuoteStatus
from jobs.models import Job


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def dashboard_stats(request):
    user = request.user
    today = timezone.now().date()
    month_start = today.replace(day=1)

    # Base querysets scoped to this user
    invoices = Invoice.objects.filter(client__user=user, archived=False)
    quotes = Quote.objects.filter(client__user=user, archived=False)
    jobs = Job.objects.filter(client__user=user, archived=False)

    # Outstanding — sent but not paid
    outstanding = invoices.filter(status=InvoiceStatus.SENT)
    outstanding_amount = outstanding.aggregate(total=Sum("subtotal"))[
        "total"
    ] or Decimal("0.00")

    # Add VAT to outstanding amount
    outstanding_total = sum(Decimal(inv.total_due) for inv in outstanding)

    # Overdue — sent and past due date
    overdue = invoices.filter(status=InvoiceStatus.SENT, due_date__lt=today)
    overdue_total = sum(Decimal(inv.total_due) for inv in overdue)

    # This month invoiced
    month_invoices = invoices.filter(issue_date__gte=month_start)
    total_invoiced_month = sum(Decimal(inv.total_due) for inv in month_invoices)

    # Paid this month
    paid_month = invoices.filter(status=InvoiceStatus.PAID, issue_date__gte=month_start)
    paid_month_total = sum(Decimal(inv.total_due) for inv in paid_month)

    # Open quotes — sent, not expired
    open_quotes = quotes.filter(status=QuoteStatus.SENT, expiry_date__gte=today).count()

    # Active jobs
    active_jobs = jobs.filter(status__in=["scheduled", "in_progress"]).count()

    return Response(
        {
            "outstanding_amount": float(outstanding_total),
            "overdue_amount": float(overdue_total),
            "overdue_count": overdue.count(),
            "open_quotes": open_quotes,
            "active_jobs": active_jobs,
            "total_invoiced_month": float(total_invoiced_month),
            "paid_month": float(paid_month_total),
        }
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def dashboard_alerts(request):
    user = request.user
    today = timezone.now().date()
    soon = today + timezone.timedelta(days=7)

    alerts = []

    # Overdue invoices
    overdue_invoices = Invoice.objects.filter(
        client__user=user,
        status=InvoiceStatus.SENT,
        due_date__lt=today,
        archived=False,
    ).select_related("client")[:5]

    for inv in overdue_invoices:
        days_overdue = (today - inv.due_date).days
        alerts.append(
            {
                "type": "overdue",
                "message": f"Invoice {inv.number} ({inv.client.name}) is {days_overdue} day{'s' if days_overdue != 1 else ''} overdue",
                "id": inv.id,
                "link": f"/invoices/{inv.id}",
            }
        )

    # Quotes expiring within 7 days
    expiring_quotes = Quote.objects.filter(
        client__user=user,
        status=QuoteStatus.SENT,
        expiry_date__gte=today,
        expiry_date__lte=soon,
        archived=False,
    ).select_related("client")[:5]

    for q in expiring_quotes:
        days_left = (q.expiry_date - today).days
        alerts.append(
            {
                "type": "expiring",
                "message": f"Quote {q.number} ({q.client.name}) expires in {days_left} day{'s' if days_left != 1 else ''}",
                "id": q.id,
                "link": f"/quotes/{q.id}",
            }
        )

    # Completed jobs with no invoice
    unbilled_jobs = Job.objects.filter(
        client__user=user,
        status="completed",
        invoices__isnull=True,
        archived=False,
    ).select_related("client")[:5]

    for job in unbilled_jobs:
        alerts.append(
            {
                "type": "unbilled",
                "message": f"Job {job.number} ({job.client.name}) is complete but has no invoice",
                "id": job.id,
                "link": f"/jobs/{job.id}",
            }
        )

    return Response(alerts)
