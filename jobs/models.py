from django.db import models
from clients.models import Client


class Job(models.Model):
    number = models.CharField(max_length=20, unique=True, db_index=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="jobs")

    source_quote = models.ForeignKey(
        "quotes.Quote",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="generated_jobs",
    )

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    date_created = models.DateTimeField(auto_now_add=True)

    status = models.CharField(
        max_length=20,
        choices=[
            ("scheduled", "Scheduled"),
            ("in_progress", "In Progress"),
            ("completed", "Completed"),
            ("cancelled", "Cancelled"),
        ],
        default="scheduled",
    )
    archived = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} - {self.client.name}"
