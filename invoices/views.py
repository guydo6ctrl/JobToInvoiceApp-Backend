from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied
from .serializers import InvoiceSerializer
from .models import Invoice
from django.db.models import Q


class InvoiceViewSet(viewsets.ModelViewSet):
    serializer_class = InvoiceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Invoice.objects.filter(
            client__user=self.request.user
        ).select_related("client")

        archived = self.request.query_params.get("archived")

        if archived is not None:
            if archived.lower() == "true":
                queryset = queryset.filter(archived=True)
            elif archived.lower() == "false":
                queryset = queryset.filter(archived=False)

        client = self.request.query_params.get("client")

        if client:
            queryset = queryset.filter(Q(client__name__icontains=client))

        return queryset

    def perform_create(self, serializer):
        source_quote = serializer.validated_data.get("source_quote")

        if source_quote:
            if source_quote.client.user != self.request.user:
                raise PermissionDenied("Not your client")

        serializer.save()
