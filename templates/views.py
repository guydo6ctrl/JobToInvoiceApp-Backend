from rest_framework import viewsets
from .models import ClientItemTemplate
from .serializers import ClientItemTemplateSerializer


class ClientItemTemplateViewSet(viewsets.ModelViewSet):
    serializer_class = ClientItemTemplateSerializer
    queryset = ClientItemTemplate.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
