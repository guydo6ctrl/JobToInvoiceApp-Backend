from rest_framework import serializers

from jobs.utils import generate_job_number
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
            "number",
            "client",
            "client_id",
            "source_quote",
            "title",
            "description",
            "date_created",
            "status",
        ]
        read_only_fields = ["number"]

    def create(self, validated_data):
        validated_data["number"] = generate_job_number()

        job = Job.objects.create(**validated_data)

        return job
