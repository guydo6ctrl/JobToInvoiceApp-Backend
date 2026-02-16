from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied
from .serializers import QuoteSerializer
from .models import Quote


class QuoteViewSet(viewsets.ModelViewSet):
    serializer_class = QuoteSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Quote.objects.filter(job__client__user=self.request.user)

    def perform_create(self, serializer):
        job = serializer.validated_data["job"]
        if job.client.user != self.request.user:
            raise PermissionDenied("Not your client")
        serializer.save()
