from django.db import models
from clients.models import Client
from core.models import BaseLineItem


class QuoteStatus(models.TextChoices):
    DRAFT = "draft", "Draft"
    SENT = "sent", "Sent"
    PAID = "accepted", "Accepted"
    CANCELLED = "rejected", "Rejected"


class Quote(models.Model):
    number = models.CharField(max_length=20, unique=True, db_index=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="quotes")
    date_created = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)
    issue_date = models.DateField()
    expiry_date = models.DateField()
    status = models.CharField(
        max_length=20, choices=QuoteStatus.choices, default=QuoteStatus.DRAFT
    )


class QuoteLineItem(BaseLineItem):
    quote = models.ForeignKey(
        "Quote", on_delete=models.CASCADE, related_name="line_items"
    )
