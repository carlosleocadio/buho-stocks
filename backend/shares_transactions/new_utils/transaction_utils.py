from decimal import Decimal
from shares_transactions.models import Transaction


class TransactionsUtils:
    def get_transaction_amount(
        self,
        transaction: Transaction,
        use_portfolio_currency: bool = True,
    ) -> Decimal:
        """Get the total amount of a transaction, calculating the price
        based on the number of shares, the exchange rate and the commission

        Args:
            transaction (Transaction): A given Transaction object
            use_portfolio_currency (bool, optional): If set to portfolio, it will use the exchange
            rate stored on the transaction (Will correspond to the exchange rate
            of the portfolio's currency).
            Defaults to "True". Otherwise, there won't be any exchange rate conversion.

        Returns:
            Decimal: The total amount of the transaction
        """

        exchange_rate = 1
        if use_portfolio_currency:
            exchange_rate = transaction.exchange_rate

        total = (
            transaction.gross_price_per_share.amount * transaction.count * exchange_rate
            + transaction.total_commission.amount * exchange_rate
        )
        return total

    def get_transactions_amount(
        self, transactions: list[Transaction], use_portfolio_currency: bool = True
    ) -> Decimal:
        """Get the total amount of a list of transactions

        Args:
            transactions (list[Transaction]): A list of transactions
            use_portfolio_currency (bool, optional): If set to portfolio, it will use the exchange
            rate stored on the transaction (Will correspond to the exchange rate
            of the portfolio's currency).
            Defaults to "True". Otherwise, there won't be any exchange rate conversion.

        Returns:
            Decimal: The total amount of all the transactions
        """
        total = 0
        for item in transactions:
            total += self.get_transaction_amount(
                item, use_portfolio_currency=use_portfolio_currency
            )
        return total
