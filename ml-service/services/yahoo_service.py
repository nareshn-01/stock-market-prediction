from decimal import Decimal

import pandas as pd
import yfinance as yf

from logger import logger
from models.price_history import PriceHistory
from models.stock import Stock


class YahooService:

    # Exchange -> Yahoo Finance suffix mapping
    EXCHANGE_SUFFIX = {
        "NSE": ".NS",
        "BSE": ".BO",
        "NASDAQ": "",
        "NYSE": ""
    }

    def get_yahoo_symbol(self, stock: Stock) -> str:
        """
        Convert stock symbol to Yahoo Finance symbol.
        """

        exchange = stock.exchange.upper()

        if exchange not in self.EXCHANGE_SUFFIX:
            raise ValueError(
                f"Unsupported exchange: {stock.exchange}"
            )

        return stock.symbol + self.EXCHANGE_SUFFIX[exchange]

    def download_history(
        self,
        symbol: str,
        period: str = "1y",
        interval: str = "1d"
    ) -> pd.DataFrame:

        try:
            logger.info(f"Downloading historical data for {symbol}")

            df = yf.download(
                tickers=symbol,
                period=period,
                interval=interval,
                auto_adjust=False,
                progress=False,
                threads=False
            )

            if df.empty:
                logger.warning(f"No data found for {symbol}")
                raise ValueError(f"No data found for {symbol}")

            # Flatten MultiIndex columns
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)

            logger.info(
                f"Downloaded {len(df)} records for {symbol}"
            )

            return df

        except Exception as e:
            logger.exception(
                f"Failed to download data for {symbol}: {e}"
            )
            raise ValueError(
                f"Failed to download data for {symbol}: {e}"
            )

    def dataframe_to_entities(
        self,
        df: pd.DataFrame,
        stock: Stock,
        interval: str = "1d"
    ):

        prices = []

        for timestamp, row in df.iterrows():

            dt = timestamp.to_pydatetime()

            if dt.tzinfo is not None:
                dt = dt.replace(tzinfo=None)

            # Skip incomplete rows
            if row[["Open", "High", "Low", "Close", "Volume"]].isnull().any():
                continue

            price = PriceHistory(
                stock_id=stock.id,
                timestamp=dt,
                open=Decimal(str(round(float(row["Open"]), 2))),
                high=Decimal(str(round(float(row["High"]), 2))),
                low=Decimal(str(round(float(row["Low"]), 2))),
                close=Decimal(str(round(float(row["Close"]), 2))),
                volume=int(row["Volume"]),
                interval=interval
            )

            prices.append(price)

        logger.info(
            f"Converted {len(prices)} records for {stock.symbol}"
        )

        return prices