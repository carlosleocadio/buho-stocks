import logging
from shares_transactions.models import SharesTransaction

logger = logging.getLogger("buho_backend")


class PortfolioUtils:
    def get_portfolio_first_year(self, portfolio_id, user_id):
        """_summary_

        Args:
            portfolio_id (_type_): _description_
            user_id (_type_): _description_

        Returns:
            _type_: _description_
        """
        query = SharesTransaction.objects.filter(
            company__portfolio=portfolio_id, user=user_id, company__is_closed=False
        ).order_by("transaction_date")
        if query.exists():
            return query[0].transaction_date.year
        return None
