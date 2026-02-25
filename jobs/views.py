from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied
from jobs.serializers import JobSerializer
from jobs.models import Job


class JobViewSet(viewsets.ModelViewSet):
    serializer_class = JobSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = Job.objects.filter(client__user=self.request.user)

        archived = self.request.query_params.get("archived")

        if archived is not None:
            if archived.lower() == "true":
                queryset = queryset.filter(archived=True)
            elif archived.lower() == "false":
                queryset = queryset.filter(archived=False)

        return queryset

    def perform_create(self, serializer):
        client = serializer.validated_data["client"]

        if client.user != self.request.user:
            raise PermissionDenied("Not your client")

        serializer.save()
