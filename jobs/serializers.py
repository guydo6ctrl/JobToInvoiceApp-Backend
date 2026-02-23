from rest_framework import serializers

from clients.models import Client
from .models import Job


class JobClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ["id", "name"]


class JobSerializer(serializers.ModelSerializer):
    client = JobClientSerializer(read_only=True)
    client_id = serializers.PrimaryKeyRelatedField(
        queryset=Client.objects.all(),
        write_only=True,
        source="client",
    )

    class Meta:
        model = Job
        fields = [
            "id",
            "client",
            "client_id",
            "source_quote",
            "title",
            "description",
            "date_created",
            "status",
        ]
