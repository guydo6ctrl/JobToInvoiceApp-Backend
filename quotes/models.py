from django.db import models
from invoices.models import BaseDocument, BaseLineItem
from jobs.models import Job


class Quote(BaseDocument):
    expiry_date = models.DateField()
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="quotes")


class QuoteLineItem(BaseLineItem):
    quote = models.ForeignKey(
        Quote, on_delete=models.CASCADE, related_name="line_items"
    )
