from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied
from .serializers import InvoiceSerializer
from .models import Invoice


class InvoiceViewSet(viewsets.ModelViewSet):
    serializer_class = InvoiceSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Invoice.objects.filter(client__user=self.request.user, archived=False)

    def perform_create(self, serializer):
        source_quote = serializer.validated_data.get("source_quote")

        if source_quote:
            if source_quote.client.user != self.request.user:
                raise PermissionDenied("Not your client")

        serializer.save()
