from django.db import models
from jobs.models import Job
from core.models import BaseLineItem
from company.models import BankDetails, CompanyDetails
from clients.models import Client
from quotes.models import Quote
from decimal import Decimal


class InvoiceStatus(models.TextChoices):
    DRAFT = "draft", "Draft"
    SENT = "sent", "Sent"
    PAID = "paid", "Paid"
    CANCELLED = "cancelled", "Cancelled"


class Invoice(models.Model):
    number = models.CharField(max_length=20, db_index=True)
    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, related_name="invoices"
    )
    description = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    payment_instructions = models.TextField(blank=True)
    payment_details = models.ForeignKey(
        BankDetails,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="invoices",
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
    date_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20, choices=InvoiceStatus.choices, default=InvoiceStatus.DRAFT
    )
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    vat_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        choices=[
            (Decimal("0.00"), "0%"),
            (Decimal("5.00"), "5%"),
            (Decimal("20.00"), "20%"),
        ],
        default=Decimal("20.00"),
    )

    archived = models.BooleanField(default=False)

    @property
    def vat_amount(self):
        if not self.client.user.company.is_vat_registered:
            return Decimal("0.00")
        return (self.subtotal * self.vat_rate / Decimal("100")).quantize(
            Decimal("0.01")
        )

    @property
    def total_due(self):
        total = self.subtotal + self.vat_amount
        return f"{total:.2f}"

    @property
    def vat_display(self):
        return int(self.vat_rate)

    def update_invoice_totals(self):
        self.subtotal = sum(item.total for item in self.line_items.all())
        self.save()


class InvoiceLineItem(BaseLineItem):
    invoice = models.ForeignKey(
        "Invoice", on_delete=models.CASCADE, related_name="line_items"
    )
