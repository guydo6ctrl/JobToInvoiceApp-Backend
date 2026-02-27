from rest_framework import serializers
from .models import BankDetails, CompanyDetails


class CompanyDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyDetails
        fields = [
            "id",
            "name",
            "email",
            "phone",
            "address_line",
            "town_or_city",
            "postcode",
            "country",
        ]
        read_only_fields = ["id"]


class BankDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankDetails
        fields = [
            "id",
            "bank_name",
            "account_number",
            "sort_code",
            "payment_instructions",
            "is_default",
        ]
        read_only_fields = ["id"]

    
