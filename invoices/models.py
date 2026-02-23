from django.db import models
from jobs.models import Job
from core.models import BaseLineItem
from clients.models import Client
from quotes.models import Quote


class InvoiceStatus(models.TextChoices):
    DRAFT = "draft", "Draft"
    SENT = "sent", "Sent"
    PAID = "paid", "Paid"
    CANCELLED = "cancelled", "Cancelled"


class Invoice(models.Model):
    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, related_name="invoices"
    )
    job = models.ForeignKey(
        Job, on_delete=models.SET_NULL, null=True, blank=True, related_name="invoices"
    )
    source_quote = models.ForeignKey(
        Quote,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="generated_invoices",
    )
    due_date = models.DateField()
    issue_date = models.DateField()
    status = models.CharField(
        max_length=20, choices=InvoiceStatus.choices, default=InvoiceStatus.DRAFT
    )
    archived = models.BooleanField(default=False)


class InvoiceLineItem(BaseLineItem):
    invoice = models.ForeignKey(
        "Invoice", on_delete=models.CASCADE, related_name="line_items"
    )
