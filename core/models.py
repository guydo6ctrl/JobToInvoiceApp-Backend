from django.db import models


class LineItemType(models.TextChoices):
    LABOUR = "Labour", "Labour"
    MATERIALS = "Materials", "Materials"
    MISCELLANEOUS = "Miscellaneous", "Miscellaneous"


class BaseLineItem(models.Model):
    name = models.CharField(max_length=150)
    description = models.CharField(max_length=255)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.CharField(
        max_length=20, choices=LineItemType.choices, default=LineItemType.MATERIALS
    )

    class Meta:
        abstract = True
