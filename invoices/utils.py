from django.utils import timezone
from .models import Invoice


def generate_invoice_number():
    year = timezone.now().year
    count = Invoice.objects.filter(date_created__year=year).count() + 1
    return f"INV-{year}-{count:04d}"
