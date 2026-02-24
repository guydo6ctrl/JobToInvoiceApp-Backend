from django.utils import timezone
from .models import Quote


def generate_quote_number():
    year = timezone.now().year
    count = Quote.objects.filter(date_created__year=year).count() + 1
    return f"Q-{year}-{count:04d}"
