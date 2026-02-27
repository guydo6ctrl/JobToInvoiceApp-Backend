from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions, filters
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from invoices.services import generate_document_pdf

from .serializers import QuoteSerializer
from .models import Quote


class QuoteViewSet(viewsets.ModelViewSet):
    serializer_class = QuoteSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["client", "status"]
    search_fields = ["number", "client__name", "status"]
    ordering_fields = ["id", "issue_date", "expiry_date", "created_at"]
    ordering = ["-id"]

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

        return queryset

    def perform_create(self, serializer):
        client_id = serializer.validated_data["client"]
        if client_id.user != self.request.user:
            raise PermissionDenied("Not your client")
        serializer.save()


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def quote_download_view(request, quote_id):
    quote = get_object_or_404(Quote, id=quote_id, client__user=request.user)
    pdf_file = generate_document_pdf("quote", Quote)

    response = HttpResponse(pdf_file, content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="Quote-{quote.id}.pdf"'
    return response
