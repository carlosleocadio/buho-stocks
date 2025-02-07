from datetime import date
from decimal import Decimal
import logging
from buho_backend.transaction_types import TransactionType
from shares_transactions.models import SharesTransaction
from shares_transactions.new_utils.transaction_utils import TransactionsUtils

logger = logging.getLogger("buho_backend")


class SharesTransactionsUtils:
    def __init__(
        self,
        shares_transactions: list[SharesTransaction],
        use_portfolio_currency: bool = True,
    ):
        self.shares_transactions = shares_transactions
        self.use_portfolio_currency = use_portfolio_currency

    def _get_transactions_query(
        self, year: int, use_accumulated: bool = False, only_buy: bool = False
    ):
        """Get the transactions query for a given year based on the parameters.

        Args:
            year (int): Year to get the transactions.
            use_accumulated (bool, optional): Whether or not to get the accumulated transactions
            until the given year. Defaults to False.
            only_buy (bool, optional): Whether or not to get only the transactions of BUY type.
            Defaults to False.

        Returns:
            _type_: _description_
        """
        query = self.shares_transactions
        if only_buy:
            query = query.filter(type=TransactionType.BUY)

        if use_accumulated:
            query = query.filter(transaction_date__year__lte=year)
        else:
            query = query.filter(transaction_date__year=year)

        return query

    def _get_sell_transactions_query(
        self,
        year: int,
        use_accumulated: bool = False,
    ):
        """[summary]

        Args:
            filter (str, optional): accumulated to obtain the accumulated values.
            Otherwhise will get the values for a give year or all Defaults to None.

        Returns:
            [type]: [description]
        """
        query = self.shares_transactions
        query = query.filter(type=TransactionType.SELL)

        if use_accumulated:
            query = query.filter(transaction_date__year__lte=year)
        else:
            query = query.filter(transaction_date__year=year)

        return query

    def _get_buy_transactions_query(
        self,
        year: int,
        use_accumulated: bool = False,
    ) -> list[SharesTransaction]:
        query = self.shares_transactions
        query = query.filter(type=TransactionType.BUY)

        if use_accumulated:
            query = query.filter(transaction_date__year__lte=year)
        else:
            query = query.filter(transaction_date__year=year)

        return query

    def get_invested_on_year(self, year: int) -> Decimal:
        """Get the total invested on a given year.

        Args:
            year (int): Year (2019, 2020, etc) to get the total invested.

        Returns:
            Decimal: The total invested amount.
        """
        total = 0
        query = self._get_buy_transactions_query(year)
        transaction_utils = TransactionsUtils()
        total = transaction_utils.get_transactions_amount(
            query, use_portfolio_currency=self.use_portfolio_currency
        )
        return total

    def get_accumulated_investment_until_year(self, year: int) -> Decimal:
        total = 0
        query = self._get_buy_transactions_query(year, use_accumulated=True)
        transaction_utils = TransactionsUtils()
        total = transaction_utils.get_transactions_amount(
            query, use_portfolio_currency=self.use_portfolio_currency
        )
        return total

    def get_accumulated_investment_until_current_year(self) -> Decimal:
        year = date.today().year
        total = self.get_accumulated_investment_until_year(year)
        return total

    def get_shares_count_until_year(self, year: int) -> int:
        """Get the total number of shares of the company for all the years
        or until a given year (accumulated value).

        Args:
            year (int): The latest year to get the accumulated value.

        Returns:
            int: Total number of shares
        """
        total = 0
        query = self._get_transactions_query(year, use_accumulated=True)

        for item in query:
            if item.type == TransactionType.BUY:
                total += item.count
            else:
                total -= item.count
        return total

    def get_shares_count_on_year(self, year: int) -> int:
        """Get the total number of shares of the company for all the years
        or until a given year (accumulated value).

        Args:
            year (int): The year to get the shares count.

        Returns:
            int: Total shares count
        """
        total = 0
        query = self._get_transactions_query(year)

        for item in query:
            if item.type == TransactionType.BUY:
                total += item.count
            else:
                total -= item.count
        return total

    def get_shares_count_until_current_year(self) -> int:
        year = date.today().year
        total = self.get_shares_count_until_year(year)
        return total

    def get_accumulated_return_from_sales_until_year(self, year: int) -> Decimal:
        total = 0
        if year == "all":
            year = date.today().year
        query = self._get_sell_transactions_query(year, use_accumulated=True)
        transactions_utils = TransactionsUtils()
        total = transactions_utils.get_transactions_amount(
            query, use_portfolio_currency=self.use_portfolio_currency
        )
        logger.debug(f"Total accumulated return from sales: {total}")
        return total
