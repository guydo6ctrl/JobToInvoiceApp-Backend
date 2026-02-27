from rest_framework import serializers

from quotes.utils import generate_quote_number
from clients.models import Client
from .models import Quote, QuoteLineItem


class QuoteLineItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuoteLineItem
        fields = ["id", "name", "description", "quantity", "unit_price", "type"]
        read_only_fields = ["id"]


class QuoteClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ["id", "name"]


class QuoteSerializer(serializers.ModelSerializer):
    client = QuoteClientSerializer(read_only=True)
    client_id = serializers.PrimaryKeyRelatedField(
        queryset=Client.objects.all(),
        write_only=True,
        source="client",
    )
    status_display = serializers.CharField(source="get_status_display", read_only=True)
    issue_date = serializers.DateField(format="%d-%m-%Y")
    expiry_date = serializers.DateField(format="%d-%m-%Y")
    line_items = QuoteLineItemSerializer(many=True)

    class Meta:
        model = Quote
        fields = [
            "id",
            "number",
            "client",
            "client_id",
            "description",
            "issue_date",
            "expiry_date",
            "line_items",
            "status",
            "status_display",
            "archived",
        ]
        read_only_fields = ["number"]

    def create(self, validated_data):

        line_items_data = validated_data.pop("line_items", [])

        validated_data["number"] = generate_quote_number()

        quote = Quote.objects.create(**validated_data)

        for item_data in line_items_data:
            QuoteLineItem.objects.create(quote=quote, **item_data)

        quote.update_quote_totals()

        return quote

    def update(self, instance, validated_data):
        line_items_data = validated_data.pop("line_items", None)

        # Update quote fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update line items if provided
        if line_items_data is not None:
            instance.line_items.all().delete()
            for item_data in line_items_data:
                QuoteLineItem.objects.create(quote=instance, **item_data)

        instance.update_quote_totals()

        return instance
