from rest_framework import serializers
from buho_backend.serializers import UserFilteredPrimaryKeyRelatedField
from buho_backend.validators import validate_ownership
from companies.models import Company
from dividends_transactions.models import DividendsTransaction
from djmoney.contrib.django_rest_framework import MoneyField


class DividendsTransactionSerializer(serializers.ModelSerializer):
    company = UserFilteredPrimaryKeyRelatedField(
        queryset=Company.objects, many=False, read_only=False
    )

    gross_price_per_share = MoneyField(max_digits=12, decimal_places=3)
    gross_price_per_share_currency = serializers.CharField(max_length=50)

    total_commission = MoneyField(max_digits=12, decimal_places=3)
    total_commission_currency = serializers.CharField(max_length=50)

    notes = serializers.CharField(allow_null = True, required=False)

    class Meta:
        model = DividendsTransaction
        fields = [
            "id",
            "count",
            "exchange_rate",
            "transaction_date",
            "gross_price_per_share",
            "gross_price_per_share_currency",
            "total_commission",
            "total_commission_currency",
            "company",
            "notes",
            "date_created",
            "last_updated",
        ]

    def validate(self, attrs):
        company = attrs["company"]
        validate_ownership(self.context, company, Company)
        return attrs
