import datetime
from decimal import Decimal
from faker import Faker
from rest_framework.test import APITestCase
from auth.tests.factory import UserFactory
from buho_backend.transaction_types import TransactionType
from companies.tests.factory import CompanyFactory
import logging

from shares_transactions.tests.factory import SharesTransactionFactory
from shares_transactions.utils import SharesTransactionsUtils


logger = logging.getLogger("buho_backend")


class SharesCountTestCase(APITestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.user_saved = UserFactory.create()
        cls.faker_obj = Faker()
        # Create company
        # Add shares
        cls.company = CompanyFactory.create(user=cls.user_saved)
        cls.shares_count = 0
        cls.total_amount = 0
        cls.total_transactions = 0
        cls.years = [2018, 2020, 2021, datetime.date.today().year]
        cls.counts = [10, 20, 30, 40, 50]
        cls.accumulated_counts = [10, 30, 60, 100, 150]
        cls.prices = [Decimal(10), Decimal(20), Decimal(30), Decimal(40), Decimal(50)]
        cls.exchange_rate = 0.5
        cls.commissions = [Decimal(1), Decimal(2), Decimal(3), Decimal(4), Decimal(5)]
        cls.prices_times_counts = [
            10 * 10 * cls.exchange_rate + cls.exchange_rate * 1,
            20 * 20 * cls.exchange_rate + cls.exchange_rate * 2,
            30 * 30 * cls.exchange_rate + cls.exchange_rate * 3,
            40 * 40 * cls.exchange_rate + cls.exchange_rate * 4,
            50 * 50 * cls.exchange_rate + cls.exchange_rate * 5,
        ]
        cls.sell_counts = [1, 2, 3, 4, 5]
        cls.sell_prices = [
            Decimal(5),
            Decimal(10),
            Decimal(15),
            Decimal(20),
            Decimal(25),
        ]
        cls.accumulated_counts_after_sell = [9, 27, 54, 90, 135]

        for index in range(0, len(cls.years)):
            first_datetime = datetime.datetime.strptime(
                f"{cls.years[index]}-01-01", "%Y-%m-%d"
            )
            SharesTransactionFactory.create(
                user=cls.user_saved,
                company=cls.company,
                gross_price_per_share_currency=cls.company.base_currency,
                total_commission_currency=cls.company.base_currency,
                count=cls.counts[index],
                type=TransactionType.BUY,
                gross_price_per_share=cls.prices[index],
                exchange_rate=cls.exchange_rate,
                total_commission=cls.commissions[index],
                transaction_date=datetime.date(
                    first_datetime.year, first_datetime.month, first_datetime.day
                ),
            )
            cls.shares_count += cls.counts[index]
            cls.total_transactions += 1

    # def setUp(self):
    #     pass

    def test_get_transactions_count(self):
        self.assertEqual(
            len(self.company.shares_transactions.all()), self.total_transactions
        )

    def test_get_shares_count_for_all(self):
        utils = SharesTransactionsUtils(self.company.shares_transactions)
        self.assertEqual(utils.get_shares_count_until_current_year(), self.shares_count)

    def test_get_shares_count_for_year(self):
        for index in range(0, len(self.years)):
            utils = SharesTransactionsUtils(self.company.shares_transactions)
            self.assertEqual(
                utils.get_shares_count_on_year(self.years[index]),
                self.counts[index],
            )

    def test_get_shares_count_with_sells(self):
        for index in range(0, len(self.years)):
            first_datetime = datetime.datetime.strptime(
                f"{self.years[index]}-01-01", "%Y-%m-%d"
            )
            SharesTransactionFactory.create(
                user=self.user_saved,
                company=self.company,
                gross_price_per_share=self.sell_prices[index],
                gross_price_per_share_currency=self.company.base_currency,
                total_commission=self.commissions[index],
                total_commission_currency=self.company.base_currency,
                count=self.sell_counts[index],
                type=TransactionType.SELL,
                exchange_rate=self.exchange_rate,
                transaction_date=datetime.date(
                    first_datetime.year, first_datetime.month, first_datetime.day
                ),
            )
            self.shares_count -= self.sell_counts[index]
            self.total_transactions += 1
        self.assertEqual(
            len(self.company.shares_transactions.all()), self.total_transactions
        )

        # utils = SharesTransactionsUtils(self.company.shares_transactions)
        # self.assertEqual(
        #     utils.get_accumulated_investment_until_current_year(), self.shares_count
        # )

        for index in range(0, len(self.years)):
            utils = SharesTransactionsUtils(self.company.shares_transactions)

            self.assertEqual(
                utils.get_shares_count_until_year(self.years[index]),
                self.accumulated_counts_after_sell[index],
            )
