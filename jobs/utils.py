from django.utils import timezone
from .models import Job


def generate_job_number():
    year = timezone.now().year
    count = Job.objects.filter(date_created__year=year).count() + 1
    return f"J-{year}-{count:04d}"
