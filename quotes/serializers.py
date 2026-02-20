from rest_framework import serializers
from .models import Quote, QuoteLineItem


class QuoteLineItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuoteLineItem
        fields = ["name", "description", "quantity", "unit_price"]


class QuoteSerializer(serializers.ModelSerializer):
    issue_date = serializers.DateField(format="%d-%m-%Y")
    expiry_date = serializers.DateField(format="%d-%m-%Y")
    line_items = QuoteLineItemSerializer(many=True)

    class Meta:
        model = Quote
        fields = [
            "id",
            "client",
            "description",
            "issue_date",
            "expiry_date",
            "line_items",
            "status",
        ]

    def create(self, validated_data):

        line_items_data = validated_data.pop("line_items", [])
        quote = Quote.objects.create(**validated_data)

        for item_data in line_items_data:
            QuoteLineItem.objects.create(quote=quote, **item_data)

        return quote
