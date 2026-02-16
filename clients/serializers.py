from rest_framework import serializers
from clients.models import Client


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ["name", "email", "phone", "address"]

        def create(self, validated_data):
            user = self.context["request"].user
            return Client.objects.create(user=user, **validated_data)
