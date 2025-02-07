import logging

from rest_framework.fields import SerializerMethodField
from rest_framework import serializers
from currencies.models import Currency
from currencies.serializers import CurrencySerializer
from dividends_transactions.models import DividendsTransaction
from dividends_transactions.serializers import DividendsTransactionSerializer
from buho_backend.serializers import UserFilteredPrimaryKeyRelatedField
from buho_backend.validators import validate_ownership
from portfolios.models import Portfolio
from portfolios.serializers_lite import PortfolioSerializerLite
from companies.models import Company
from rights_transactions.serializers import RightsTransactionSerializer
from sectors.models import Sector
from sectors.serializers import SectorSerializerGet
from markets.models import Market
from markets.serializers import MarketSerializer
from shares_transactions.serializers import SharesTransactionSerializer
from shares_transactions.models import SharesTransaction
from drf_extra_fields.fields import Base64ImageField
from stats.models.company_stats import CompanyStatsForYear
from stats.serializers.company_stats import CompanyStatsForYearSerializer

logger = logging.getLogger("buho_backend")


class CompanySerializer(serializers.ModelSerializer):
    market = serializers.PrimaryKeyRelatedField(
        queryset=Market.objects, many=False, read_only=False
    )
    sector = serializers.PrimaryKeyRelatedField(
        queryset=Sector.objects, many=False, read_only=False
    )
    portfolio = UserFilteredPrimaryKeyRelatedField(
        queryset=Portfolio.objects, many=False, read_only=False
    )

    logo = Base64ImageField(
        max_length=None, use_url=True, allow_null=True, required=False
    )
    all_stats = serializers.SerializerMethodField()
    last_transaction_month = serializers.SerializerMethodField()
    last_dividend_month = serializers.SerializerMethodField()
    sector_name = serializers.CharField(source="sector.name", read_only=True)

    class Meta:
        model = Company
        fields = [
            "id",
            "alt_tickers",
            "base_currency",
            "broker",
            "color",
            "country_code",
            "description",
            "dividends_currency",
            "is_closed",
            "isin",
            "logo",
            "market",
            "name",
            "portfolio",
            "sector",
            "sector_name",
            "ticker",
            "url",
            "all_stats",
            "date_created",
            "last_updated",
            "last_transaction_month",
            "last_dividend_month",
        ]

    def validate(self, attrs):
        portfolio = attrs["portfolio"]

        validate_ownership(self.context, portfolio, Portfolio)
        return attrs

    def get_all_stats(self, obj):
        query = CompanyStatsForYear.objects.filter(
            company=obj.id, user=obj.user, year=9999
        )
        if query.exists():
            serializer = CompanyStatsForYearSerializer(query[0])
            return serializer.data
        return None

    def get_last_transaction_month(self, obj):
        query = SharesTransaction.objects.filter(
            company_id=obj.id, user=obj.user
        ).order_by("transaction_date")
        if query.exists():
            last_element = query[len(query) - 1]
            return last_element.transaction_date
        return None

    def get_last_dividend_month(self, obj):
        query = DividendsTransaction.objects.filter(
            company_id=obj.id, user=obj.user
        ).order_by("transaction_date")
        if query.exists():
            last_element = query[len(query) - 1]
            return last_element.transaction_date
        return None


class CompanySerializerGet(CompanySerializer):
    base_currency = SerializerMethodField()
    dividends_currency = SerializerMethodField()

    market = MarketSerializer(many=False, read_only=True)
    sector = SectorSerializerGet(many=False, read_only=True)
    shares_transactions = SharesTransactionSerializer(many=True, read_only=True)
    rights_transactions = RightsTransactionSerializer(many=True, read_only=True)
    dividends_transactions = DividendsTransactionSerializer(many=True, read_only=True)
    portfolio = PortfolioSerializerLite(many=False, read_only=True)
    first_year = serializers.SerializerMethodField()
    last_transaction_month = serializers.SerializerMethodField()
    stats = CompanyStatsForYearSerializer(many=True, read_only=True)

    def get_base_currency(self, obj):
        currency = Currency.objects.filter(code=obj.base_currency).first()
        serialized_currency = CurrencySerializer(currency)
        return serialized_currency.data

    def get_dividends_currency(self, obj):
        currency = Currency.objects.filter(code=obj.dividends_currency).first()
        serialized_currency = CurrencySerializer(currency)
        return serialized_currency.data

    def get_logo(self, obj):
        request = self.context.get("request")
        photo_url = obj.fingerprint.url
        return request.build_absolute_uri(photo_url)

    def get_first_year(self, obj):
        query = SharesTransaction.objects.filter(
            company_id=obj.id, user=obj.user
        ).order_by("transaction_date")
        if query.exists():
            return query[0].transaction_date.year
        return None

    def get_last_transaction_month(self, obj):
        query = SharesTransaction.objects.filter(
            company_id=obj.id, user=obj.user
        ).order_by("transaction_date")
        if query.exists():
            return f"{query[len(query)-1].transaction_date.year}-{query[len(query)-1].transaction_date.month}"
        return None

    class Meta:
        model = Company
        fields = [
            "id",
            "alt_tickers",
            "base_currency",
            "broker",
            "color",
            "country_code",
            "description",
            "dividends_currency",
            "dividends_transactions",
            "isin",
            "is_closed",
            "logo",
            "market",
            "name",
            "portfolio",
            "rights_transactions",
            "sector",
            "shares_transactions",
            "ticker",
            "url",
            "stats",
            "date_created",
            "last_updated",
            "first_year",
            "last_transaction_month",
        ]
