from django.shortcuts import render
from rest_framework import viewsets, permissions
from clients.models import Client
from clients.serializers import ClientSerializer


class ClientViewSet(viewsets.ModelViewSet):
    serializer_class = ClientSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = Client.objects.filter(user = self.request.user)

        archived = self.request.query_params.get("archived")

        if archived is not None:
            if archived.lower() == "true":
                queryset = queryset.filter(archived=True)
            elif archived.lower() == "false":
                queryset = queryset.filter(archived=False)

        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
