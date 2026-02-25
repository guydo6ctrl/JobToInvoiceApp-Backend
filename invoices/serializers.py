from rest_framework import serializers

from invoices.utils import generate_invoice_number
from .models import Invoice, InvoiceLineItem
from clients.models import Client
from quotes.models import Quote


class InvoiceLineItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceLineItem
        fields = ["name", "description", "quantity", "unit_price"]


class InvoiceClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ["id", "name"]


class InvoiceSerializer(serializers.ModelSerializer):
    job_number = serializers.CharField(source="job.number", read_only=True)

    client = InvoiceClientSerializer(read_only=True)
    client_id = serializers.PrimaryKeyRelatedField(
        queryset=Client.objects.all(),
        write_only=True,
        source="client",
    )
    source_quote = serializers.PrimaryKeyRelatedField(
        queryset=Quote.objects.all(),
        required=False,
        allow_null=True,
    )
    status_display = serializers.CharField(source="get_status_display", read_only=True)
    issue_date = serializers.DateField(format="%d-%m-%Y")
    due_date = serializers.DateField(format="%d-%m-%Y")
    line_items = InvoiceLineItemSerializer(many=True)

    class Meta:
        model = Invoice
        fields = [
            "id",
            "number",
            "client",
            "client_id",
            "job",
            "job_number",
            "source_quote",
            "issue_date",
            "due_date",
            "line_items",
            "status",
            "status_display",
            "archived",
        ]
        read_only_fields = ["number"]

    def create(self, validated_data):

        line_items_data = validated_data.pop("line_items", [])

        validated_data["number"] = generate_invoice_number()

        invoice = Invoice.objects.create(**validated_data)

        for item_data in line_items_data:
            InvoiceLineItem.objects.create(invoice=invoice, **item_data)

        return invoice

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
                InvoiceLineItem.objects.create(invoice=instance, **item_data)

        return instance
