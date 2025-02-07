import logging
from exchange_rates.services.ecb_api_client import EcbApiClient
from exchange_rates.models import ExchangeRate

logger = logging.getLogger("buho_backend")


class EcbApiClientError(Exception):
    pass


class ExchangeRateService:
    def save_exchange_rate(self, data: dict) -> ExchangeRate:
        """Saves the exchange rate in the database

        Args:
            data (dict): A dictionary with the exchange rate data

        Returns:
            ExchangeRate: The saved exchange rate
        """
        exchange_rate = ExchangeRate(**data)
        exchange_rate.save()
        return exchange_rate

    def get_exchange_rate_for_date(
        self, from_currency: str, to_currency: str, transaction_date: str
    ) -> ExchangeRate:
        """Gets the exchange rate object for a given date

        Args:
            from_currency (str): Source currency
            to_currency (str): Target currency
            transaction_date (str): Date of the transaction (YYYY-MM-DD)

        Returns:
            ExchangeRate: The exchange rate object for the date
        """
        if from_currency == to_currency:
            exchange_rate = ExchangeRate(
                exchange_from=from_currency,
                exchange_to=to_currency,
                exchange_date=transaction_date,
                exchange_rate="1.000",
            )
            return exchange_rate

        try:
            exchange_rate = ExchangeRate.objects.get(
                exchange_from=from_currency,
                exchange_to=to_currency,
                exchange_date=transaction_date,
            )
            return exchange_rate

        except ExchangeRate.DoesNotExist:
            ecb_api = EcbApiClient()
            exchange_rate_dict = ecb_api.get_exchange_rate_for_date(
                from_currency, to_currency, transaction_date
            )

            if exchange_rate_dict:
                saved_exchange_rate = self.save_exchange_rate(exchange_rate_dict)
                return saved_exchange_rate

        except EcbApiClientError as error:
            logger.debug(str(error), exc_info=True)
            return None
