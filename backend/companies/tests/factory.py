import random
from factory import django, Faker, SubFactory, post_generation
from auth.tests.factory import UserFactory
from companies.models import Company
from currencies.models import get_all_currencies
from markets.tests.factory import MarketFactory
from portfolios.tests.factory import PortfolioFactory
from sectors.tests.factory import SectorFactory


class CompanyFactory(django.DjangoModelFactory):
    class Meta:
        model = Company

    name = Faker("company")
    ticker = Faker("pystr", max_chars=4)
    alt_tickers = Faker("paragraph")
    description = Faker("paragraph")
    url = Faker("url")
    color = Faker("color")
    broker = Faker("company")
    is_closed = Faker("boolean")
    country_code = Faker("country_code")

    base_currency = random.choice(get_all_currencies())["code"]
    dividends_currency = random.choice(get_all_currencies())["code"]

    user = SubFactory(UserFactory)
    sector = SubFactory(SectorFactory)
    market = SubFactory(MarketFactory)
    portfolio = SubFactory(PortfolioFactory)

    @post_generation
    def set_currencies(self, create, extracted, use_base_currency=False, **kwargs):
        if not create:
            return
        if extracted and use_base_currency:
            self.base_currency = extracted["base_currency"]
            self.dividends_currency = extracted["base_currency"]
