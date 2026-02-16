from django.db import models
from jobs.models import Job


class Status(models.TextChoices):
    DRAFT = "draft", "Draft"
    SENT = "sent", "Sent"
    PAID = "paid", "Paid"
    CANCELLED = "cancelled", "Cancelled"


class BaseDocument(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    issue_date = models.DateField()

    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.DRAFT
    )

    class Meta:
        abstract = True


class Invoice(BaseDocument):
    due_date = models.DateField()
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="invoices")


class BaseLineItem(models.Model):
    description = models.CharField(max_length=255)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        abstract = True


class InvoiceLineItem(BaseLineItem):
    invoice = models.ForeignKey(
        Invoice, on_delete=models.CASCADE, related_name="line_items"
    )
