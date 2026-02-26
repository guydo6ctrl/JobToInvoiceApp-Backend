from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied
from .serializers import QuoteSerializer
from .models import Quote


class QuoteViewSet(viewsets.ModelViewSet):
    serializer_class = QuoteSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["client", "status"]

    def get_queryset(self):
        queryset = Quote.objects.filter(client__user=self.request.user).select_related(
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

        client_name = self.request.query_params.get("client_name")
        if client_name:
            queryset = queryset.filter(client__name__icontains=client_name)

        return queryset

    def perform_create(self, serializer):
        client_id = serializer.validated_data["client"]
        if client_id.user != self.request.user:
            raise PermissionDenied("Not your client")
        serializer.save()
