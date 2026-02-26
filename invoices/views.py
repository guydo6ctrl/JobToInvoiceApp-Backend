from rest_framework import viewsets, permissions, filters
from rest_framework.exceptions import PermissionDenied
from .models import Invoice
from .serializers import InvoiceSerializer


class InvoiceViewSet(viewsets.ModelViewSet):
    serializer_class = InvoiceSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    search_fields = ["number", "client__name", "status"]
    ordering_fields = ["id"]
    ordering = ["-id"]

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

        return queryset

    def perform_create(self, serializer):
        source_quote = serializer.validated_data.get("source_quote")

        if source_quote:
            if source_quote.client.user != self.request.user:
                raise PermissionDenied("Not your client")

        serializer.save()
