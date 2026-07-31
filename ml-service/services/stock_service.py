from logger import logger

from repositories.stock_repository import StockRepository
from services.yahoo_service import YahooService


class StockService:

    """
    Handles downloading and updating stock price history.
    """

    def __init__(
        self,
        stock_repository: StockRepository,
        yahoo_service: YahooService
    ):
        self.stock_repository = stock_repository
        self.yahoo_service = yahoo_service

    # ---------------------------------------------------------
    # Update Single Stock
    # ---------------------------------------------------------

    def update_stock(
        self,
        stock,
        period: str = "10y",
        interval: str = "1d"
    ):

        yahoo_symbol = self.yahoo_service.get_yahoo_symbol(
            stock
        )

        logger.info(
            f"Updating {stock.symbol}"
        )

        df = self.yahoo_service.download_history(
            yahoo_symbol,
            period=period,
            interval=interval
        )

        prices = self.yahoo_service.dataframe_to_entities(
            df,
            stock,
            interval
        )

        existing = self.stock_repository.get_existing_timestamps(
            stock.id
        )

        new_prices = [
            price
            for price in prices
            if price.timestamp not in existing
        ]

        if not new_prices:

            logger.info(
                f"{stock.symbol} already up to date."
            )

            return {
                "symbol": stock.symbol,
                "added": 0,
                "total": len(prices)
            }

        self.stock_repository.save_all_prices(
            new_prices
        )

        self.stock_repository.commit()

        logger.info(
            f"{stock.symbol}: inserted {len(new_prices)} rows."
        )

        return {
            "symbol": stock.symbol,
            "added": len(new_prices),
            "total": len(prices)
        }

    # ---------------------------------------------------------
    # Update All Stocks
    # ---------------------------------------------------------

    def update_all_stocks(
        self,
        period: str = "10y",
        interval: str = "1d"
    ):

        stocks = self.stock_repository.get_all()

        results = []

        for stock in stocks:

            try:

                result = self.update_stock(
                    stock,
                    period,
                    interval
                )

                results.append(result)

            except Exception as ex:

                logger.exception(ex)

                results.append({

                    "symbol": stock.symbol,

                    "error": str(ex)

                })

        return results

    # ---------------------------------------------------------
    # Refresh Single Stock
    # ---------------------------------------------------------

    def refresh_stock(
        self,
        stock
    ):
        """
        Refresh using default settings.
        """

        return self.update_stock(
            stock,
            period="10y",
            interval="1d"
        )

    # ---------------------------------------------------------
    # Refresh All Stocks
    # ---------------------------------------------------------

    def refresh_all_stocks(
        self
    ):
        """
        Refresh all stocks using default settings.
        """

        return self.update_all_stocks(
            period="10y",
            interval="1d"
        )