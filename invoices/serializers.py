from rest_framework import serializers
from .models import Invoice, InvoiceLineItem
from quotes.models import Quote


class InvoiceLineItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceLineItem
        fields = ["name", "description", "quantity", "unit_price"]


class InvoiceSerializer(serializers.ModelSerializer):
    source_quote = serializers.PrimaryKeyRelatedField(
        queryset=Quote.objects.all(),
        required=False,
        allow_null=True,
    )
    issue_date = serializers.DateField(format="%d-%m-%Y")
    due_date = serializers.DateField(format="%d-%m-%Y")
    line_items = InvoiceLineItemSerializer(many=True)

    class Meta:
        model = Invoice
        fields = [
            "id",
            "client",
            "source_quote",
            "issue_date",
            "due_date",
            "line_items",
            "status",
            "archived",
        ]

    def create(self, validated_data):

        line_items_data = validated_data.pop("line_items", [])
        invoice = Invoice.objects.create(**validated_data)

        for item_data in line_items_data:
            InvoiceLineItem.objects.create(invoice=invoice, **item_data)

        return invoice
