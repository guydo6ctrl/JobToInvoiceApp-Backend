from rest_framework import serializers
from .models import Job


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = [
            "id",
            "client",
            "source_quote",
            "title",
            "description",
            "date_created",
            "status",
        ]
