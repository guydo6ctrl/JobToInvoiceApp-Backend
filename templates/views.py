from rest_framework import viewsets, permissions
from .models import ClientItemTemplate
from .serializers import ClientItemTemplateSerializer


class ClientItemTemplateViewSet(viewsets.ModelViewSet):
    serializer_class = ClientItemTemplateSerializer
    queryset = ClientItemTemplate.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
