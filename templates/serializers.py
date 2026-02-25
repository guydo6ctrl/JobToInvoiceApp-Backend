from rest_framework import serializers
from .models import ClientItemTemplate


class ClientItemTemplateSerializer(serializers.ModelSerializer):

    class Meta:
        model = ClientItemTemplate
        fields = ["id", "name", "description", "unit_price", "type"]
        read_only_fields = ["id"]
