from django.db import models
from core.models import BaseLineItem, Status
from clients.models import Client
from quotes.models import Quote


class Invoice(models.Model):
    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, related_name="invoices"
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
        max_length=20, choices=Status.choices, default=Status.DRAFT
    )


class InvoiceLineItem(BaseLineItem):
    invoice = models.ForeignKey(
        "Invoice", on_delete=models.CASCADE, related_name="line_items"
    )
