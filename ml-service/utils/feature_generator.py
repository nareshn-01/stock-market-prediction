import pandas as pd
from typing import List

from repositories.stock_repository import StockRepository
from repositories.technical_indicator_repository import (
    TechnicalIndicatorRepository
)


class FeatureGenerator:
    """
    Generates machine learning feature datasets by combining
    stock OHLCV data with technical indicators.
    """

    FEATURE_COLUMNS: List[str] = [
        "open",
        "high",
        "low",
        "close",
        "volume",

        "sma_20",
        "sma_50",
        "sma_200",

        "ema_12",
        "ema_26",

        "macd",
        "macd_signal",
        "macd_histogram",

        "rsi_14",

        "bb_upper",
        "bb_middle",
        "bb_lower",

        "atr_14",

        "plus_di_14",
        "minus_di_14",
        "dx_14",
        "adx_14"
    ]

    def __init__(
        self,
        stock_repository: StockRepository,
        indicator_repository: TechnicalIndicatorRepository
    ):
        self.stock_repository = stock_repository
        self.indicator_repository = indicator_repository

    def generate(self, symbol: str) -> pd.DataFrame:
        """
        Returns a feature dataframe ready for model training.
        """

        stocks = self.stock_repository.get_by_symbol(symbol)

        indicators = self.indicator_repository.get_by_symbol(symbol)

        if not stocks:
            raise ValueError(f"No stock data found for {symbol}")

        if not indicators:
            raise ValueError(
                f"No technical indicators found for {symbol}"
            )

        stock_df = pd.DataFrame(
            [
                {
                    "date": s.date,
                    "open": s.open,
                    "high": s.high,
                    "low": s.low,
                    "close": s.close,
                    "volume": s.volume
                }
                for s in stocks
            ]
        )

        indicator_df = pd.DataFrame(
            [
                {
                    "date": i.date,

                    "sma_20": i.sma_20,
                    "sma_50": i.sma_50,
                    "sma_200": i.sma_200,

                    "ema_12": i.ema_12,
                    "ema_26": i.ema_26,

                    "macd": i.macd,
                    "macd_signal": i.macd_signal,
                    "macd_histogram": i.macd_histogram,

                    "rsi_14": i.rsi_14,

                    "bb_upper": i.bb_upper,
                    "bb_middle": i.bb_middle,
                    "bb_lower": i.bb_lower,

                    "atr_14": i.atr_14,

                    "plus_di_14": i.plus_di_14,
                    "minus_di_14": i.minus_di_14,
                    "dx_14": i.dx_14,
                    "adx_14": i.adx_14
                }
                for i in indicators
            ]
        )

        df = pd.merge(
            stock_df,
            indicator_df,
            on="date",
            how="inner"
        )

        df.sort_values("date", inplace=True)

        df["target"] = df["close"].shift(-1)

        df.dropna(inplace=True)

        df.reset_index(drop=True, inplace=True)

        return df

    def get_feature_columns(self) -> List[str]:
        """
        Returns feature column names.
        """

        return self.FEATURE_COLUMNS