from django.db import models
from users.models import User
from core.models import LineItemType


class ClientItemTemplate(models.Model):

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="item_templates"
    )

    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)

    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    type = models.CharField(
        max_length=20, choices=LineItemType.choices, default=LineItemType.MATERIALS
    )
