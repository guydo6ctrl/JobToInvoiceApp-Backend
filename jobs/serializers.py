from rest_framework import serializers

from jobs.utils import generate_job_number
from clients.models import Client
from .models import Job


class JobClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ["id", "name"]


class JobSerializer(serializers.ModelSerializer):
    quote_number = serializers.CharField(source="source_quote.number", read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)

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
            "number",
            "client",
            "client_id",
            "source_quote",
            "quote_number",
            "title",
            "description",
            "date_created",
            "status_display",
            "status",
        ]
        read_only_fields = ["number", "quote_number"]

    def create(self, validated_data):
        validated_data["number"] = generate_job_number()

        job = Job.objects.create(**validated_data)

        return job
