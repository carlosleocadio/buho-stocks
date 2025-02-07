from decimal import Decimal
from django.urls import reverse
from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from auth.tests.factory import UserFactory
from companies.tests.factory import CompanyFactory
import logging
import factory
from dividends_transactions.models import DividendsTransaction

from dividends_transactions.tests.factory import DividendsTransactionFactory

logger = logging.getLogger("buho_backend")


class DividendsTransactionsListTestCase(APITestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.user_saved = UserFactory.create()
        cls.token, _ = Token.objects.get_or_create(user=cls.user_saved)
        cls.faker_obj = Faker()

    def setUp(self):
        self.client = APIClient(HTTP_AUTHORIZATION="Token " + self.token.key)

    def test_get_rights(self):
        company = CompanyFactory.create(user=self.user_saved)
        url = reverse("dividends-transaction-list", args=[company.id])
        response = self.client.get(url)
        # Check status response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

        for _ in range(0, 4):
            DividendsTransactionFactory.create(
                user=self.user_saved,
                company=company,
                gross_price_per_share_currency=company.base_currency,
                total_commission_currency=company.base_currency,
            )

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)

class DividendsTransactionsDetailTestCase(APITestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.user_saved = UserFactory.create()
        cls.token, _ = Token.objects.get_or_create(user=cls.user_saved)
        cls.company = CompanyFactory.create(user=cls.user_saved)
        instances = []
        for _ in range(0, 4):
            instance = DividendsTransactionFactory.create(
                user=cls.user_saved,
                company=cls.company,
                gross_price_per_share_currency=cls.company.base_currency,
                total_commission_currency=cls.company.base_currency,
            )
            instances.append(instance)
        cls.instances = instances

    def setUp(self):
        self.client = APIClient(HTTP_AUTHORIZATION="Token " + self.token.key)

    def test_get_dividends(self):
        index = 0
        url = reverse("dividends-transaction-detail", args=[self.company.id, self.instances[index].id])
        response = self.client.get(url)
        # Check status response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["count"],
            self.instances[index].count,
        )
        self.assertEqual(
            Decimal(response.data["exchange_rate"]),
            self.instances[index].exchange_rate,
        )
        self.assertEqual(
            Decimal(response.data["gross_price_per_share"]),
            self.instances[index].gross_price_per_share.amount,
        )
        self.assertEqual(
            response.data["gross_price_per_share_currency"],
            str(self.instances[index].gross_price_per_share.currency),
        )
        index = len(self.instances) - 1
        url = reverse("dividends-transaction-detail", args=[self.company.id, self.instances[index].id])
        response = self.client.get(url)
        self.assertEqual(
            Decimal(response.data["total_commission"]),
            self.instances[index].total_commission.amount,
        )
        self.assertEqual(
            response.data["total_commission_currency"],
            str(self.instances[index].total_commission.currency),
        )

    def test_update_dividends_transaction(self):
        index = 0
        temp_data = factory.build(dict, FACTORY_CLASS=DividendsTransactionFactory)
        temp_data["company"] = self.company.id
        temp_data["gross_price_per_share_currency"] = self.company.base_currency
        temp_data["total_commission_currency"] = self.company.base_currency

        url = reverse("dividends-transaction-detail", args=[self.company.id, self.instances[index].id])
        response = self.client.put(url, temp_data)
        # Check status response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            Decimal(response.data["count"]),
            temp_data["count"],
        )
        self.assertEqual(
            Decimal(response.data["total_commission"]),
            temp_data["total_commission"],
        )
        self.assertEqual(
            response.data["notes"],
            temp_data["notes"],
        )

    def test_delete_transaction(self):
        url = reverse("dividends-transaction-detail", args=[self.company.id, self.instances[0].id])
        response = self.client.delete(url)
        # Check status response

        trans = DividendsTransaction.objects.all()
        self.assertEqual(len(trans), 3)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(DividendsTransaction.DoesNotExist):
            DividendsTransaction.objects.get(id=self.instances[0].id)