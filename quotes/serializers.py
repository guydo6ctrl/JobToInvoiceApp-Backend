from rest_framework import serializers
from .models import Quote


class QuoteSerializer(serializers.ModelSerializer):
    issue_date = serializers.DateField(format="%d-%m-%Y")
    issue_date = serializers.DateField(format="%d-%m-%Y")

    class Meta:
        model = Quote
        fields = ["client", "issue_date", "expiry_date", "line_items", "status"]


class QuoteLineItemSerializer(serializers.ModelSerializer):
    class Meta: 
        model = QuoteItem
