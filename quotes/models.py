from django.db import models
from clients.models import Client
from core.models import BaseLineItem, Status


class Quote(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="quotes")
    job = models.ForeignKey(
        "jobs.Job",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="invoices",
    )
    issue_date = models.DateField()
    expiry_date = models.DateField()
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.DRAFT
    )


class QuoteLineItem(BaseLineItem):
    quote = models.ForeignKey(
        "Quote", on_delete=models.CASCADE, related_name="line_items"
    )
