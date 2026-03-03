from django.utils import timezone
from django.db import transaction


def generate_job_number(company):
    current_year = timezone.now().year

    with transaction.atomic():

        # Reset sequence if new year
        if company.sequence_year != current_year:
            company.job_sequence = 0
            company.sequence_year = current_year

        company.job_sequence += 1
        company.save(update_fields=["job_sequence", "sequence_year"])

        return f"J-{current_year}-{company.job_sequence:04d}"
