from django.db import models
from clients.models import Client


class Job(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="jobs")
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} - {self.client.name}"
