from django.utils import timezone
from django.db import transaction


def generate_quote_number(company):
    current_year = timezone.now().year

    with transaction.atomic():

        # Reset sequence if new year
        if company.sequence_year != current_year:
            company.sequence = 0
            company.sequence_year = current_year

        company.quote_sequence += 1
        company.save(update_fields=["quote_sequence", "sequence_year"])

        return f"Q-{current_year}-{company.quote_sequence:04d}"
