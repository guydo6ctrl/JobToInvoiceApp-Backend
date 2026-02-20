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
        return Quote.objects.filter(client__user=self.request.user)

    def perform_create(self, serializer):
        client_id = serializer.validated_data["client"]
        if client_id.user != self.request.user:
            raise PermissionDenied("Not your client")
        serializer.save()
