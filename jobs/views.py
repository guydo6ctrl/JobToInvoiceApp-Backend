from django.shortcuts import render
from rest_framework import viewsets, permissions, filters
from rest_framework.exceptions import PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from jobs.serializers import JobSerializer
from jobs.models import Job


class JobViewSet(viewsets.ModelViewSet):
    serializer_class = JobSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["client", "status"]
    search_fields = ["number", "client__name", "status"]
    ordering_fields = ["id"]
    ordering = ["-id"]

    def get_queryset(self):
        queryset = Job.objects.filter(client__user=self.request.user).select_related(
            "client"
        )

        archived = self.request.query_params.get("archived")
        if archived is not None:
            archived = archived.lower()
            if archived in ["true", "1"]:
                queryset = queryset.filter(archived=True)
            elif archived in ["false", "0"]:
                queryset = queryset.filter(archived=False)

        client_id = self.request.query_params.get("client_id")
        if client_id:
            queryset = queryset.filter(client_id=client_id)

        return queryset

    def perform_create(self, serializer):
        client = serializer.validated_data["client"]

        if client.user != self.request.user:
            raise PermissionDenied("Not your client")

        serializer.save()
