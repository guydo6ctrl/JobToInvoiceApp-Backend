from rest_framework import serializers
from .models import ClientItemTemplate


class ClientItemTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientItemTemplate
        fields = ["name", "description", "unit_price", "type"]
