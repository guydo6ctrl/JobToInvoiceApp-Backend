from django.db import models
from config import settings


class CompanyDetails(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="company"
    )
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=50, blank=True)

    address_line = models.TextField(max_length=100, blank=True)

    town_or_city = models.TextField(max_length=100, blank=True)
    postcode = models.TextField(max_length=20, blank=True)
    country = models.TextField(max_length=80, blank=True, default="United Kingdom")


class BankDetails(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="banks"
    )
    bank_name = models.CharField(max_length=255, blank=True)
    account_number = models.CharField(max_length=50, blank=True)
    sort_code = models.CharField(max_length=20, blank=True)
    payment_instructions = models.TextField(
        blank=True, help_text="Optional instructions for clients"
    )
    is_default = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Then update other records
        if self.is_default:
            BankDetails.objects.filter(user=self.user, is_default=True).exclude(
                id=self.id
            ).update(is_default=False)
