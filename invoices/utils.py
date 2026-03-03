from django.utils import timezone
from django.db import transaction


def generate_invoice_number(company):
    current_year = timezone.now().year

    with transaction.atomic():

        # Reset sequence if new year
        if company.sequence_year != current_year:
            company.invoice_sequence = 0
            company.sequence_year = current_year

        company.invoice_sequence += 1
        company.save(update_fields=["invoice_sequence", "sequence_year"])

        return f"INV-{current_year}-{company.invoice_sequence:04d}"
