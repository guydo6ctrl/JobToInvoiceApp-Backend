from django.db import models


class LineItemType(models.TextChoices):
    LABOUR = "labour", "Labour"
    MATERIALS = "materials", "Materials"
    MISCELLANEOUS = "miscellaneous", "Miscellaneous"


class BaseLineItem(models.Model):
    description = models.CharField(max_length=255)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.CharField(
        max_length=20, choices=LineItemType.choices, default=LineItemType.MATERIALS
    )

    class Meta:
        abstract = True


class Status(models.TextChoices):
    DRAFT = "draft", "Draft"
    SENT = "sent", "Sent"
    PAID = "paid", "Paid"
    CANCELLED = "cancelled", "Cancelled"
