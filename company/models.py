from decimal import Decimal

from django.db import models
from django.conf import settings


class CompanyDetails(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="company"
    )
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=50, blank=True)

    payment_instructions = models.TextField(
        blank=True, help_text="Optional instructions for clients"
    )
    quote_terms = models.TextField(
        blank=True, help_text="Optional quoting terms for clients"
    )

    is_vat_registered = models.BooleanField(default=True)

    address_line = models.TextField(max_length=100, blank=True)

    town_or_city = models.TextField(max_length=100, blank=True)
    postcode = models.TextField(max_length=20, blank=True)
    country = models.TextField(max_length=80, blank=True, default="United Kingdom")
    quote_sequence = models.PositiveIntegerField(default=0)
    job_sequence = models.PositiveIntegerField(default=0)
    invoice_sequence = models.PositiveIntegerField(default=0)
    sequence_year = models.PositiveIntegerField(null=True, blank=True)


class BankDetails(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="banks"
    )
    bank_name = models.CharField(max_length=255, blank=True)
    account_number = models.CharField(max_length=50, blank=True)
    sort_code = models.CharField(max_length=20, blank=True)

    is_default = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not BankDetails.objects.filter(user=self.user, is_default=True).exists():
            self.is_default = True

        super().save(*args, **kwargs)

        # When updating default payments
        if self.is_default:
            BankDetails.objects.filter(user=self.user, is_default=True).exclude(
                id=self.id
            ).update(is_default=False)
