from django.shortcuts import render
from rest_framework import viewsets, permissions
from clients.models import Client
from clients.serializers import ClientSerializer


class ClientViewSet(viewsets.ModelViewSet):
    serializer_class = ClientSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Client.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
