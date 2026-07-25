from logger import logger
from models import stock
from models.stock import Stock
from repositories.stock_repository import StockRepository
from services import indicator_service
from services.yahoo_service import YahooService


class DownloadService:

    def __init__(self, repository: StockRepository):
        self.repository = repository
        self.yahoo = YahooService()

    def download_stock(self, stock: Stock):

        yahoo_symbol = self.yahoo.get_yahoo_symbol(stock)

        df = self.yahoo.download_history(yahoo_symbol)

        prices = self.yahoo.dataframe_to_entities(df, stock)

        existing_timestamps = self.repository.get_existing_timestamps(stock.id)

        new_prices = [
            price
            for price in prices
            if price.timestamp not in existing_timestamps
        ]

        if new_prices:
            self.repository.save_all_prices(new_prices)
            self.repository.commit()

        logger.info(
            f"{stock.symbol}: Downloaded={len(prices)}, Inserted={len(new_prices)}"
        )

        return {
            "symbol": stock.symbol,
            "exchange": stock.exchange,
            "yahoo_symbol": yahoo_symbol,
            "records_downloaded": len(prices),
            "records_inserted": len(new_prices)
        }