from django.shortcuts import render
from rest_framework import viewsets, permissions
from clients.models import Client
from clients.serializers import ClientSerializer
from django.db.models import Q


class ClientViewSet(viewsets.ModelViewSet):
    serializer_class = ClientSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Client.objects.filter(user=self.request.user)

        archived = self.request.query_params.get("archived")
        if archived is not None:
            if archived.lower() in ["true", "1"]:
                queryset = queryset.filter(archived=True)
            elif archived.lower() in ["false", "0"]:
                queryset = queryset.filter(archived=False)

        name = self.request.query_params.get("name")

        if name:
            queryset = queryset.filter(Q(name__icontains=name))

        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
