from rest_framework import viewsets, permissions, filters
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from core.pagination import DataPagination
from .models import Invoice
from .serializers import InvoiceSerializer
from .services import generate_document_pdf


class InvoiceViewSet(viewsets.ModelViewSet):
    serializer_class = InvoiceSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = DataPagination
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    search_fields = ["number", "client__name", "status"]
    ordering_fields = ["id", "date_created"]
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


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def invoice_download_view(request, invoice_id):
    invoice = get_object_or_404(Invoice, id=invoice_id, client__user=request.user)
    pdf_file = generate_document_pdf("invoice", invoice)

    response = HttpResponse(pdf_file, content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="Invoice-{invoice.id}.pdf"'
    return response
