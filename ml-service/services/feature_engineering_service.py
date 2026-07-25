import pandas as pd

from repositories.stock_repository import StockRepository
from repositories.technical_indicator_repository import (
    TechnicalIndicatorRepository
)


class FeatureEngineeringService:

    def __init__(
        self,
        stock_repository: StockRepository,
        indicator_repository: TechnicalIndicatorRepository
    ):
        self.stock_repository = stock_repository
        self.indicator_repository = indicator_repository

    def build_dataset(self, stock):

        prices = self._load_prices(stock)
        indicators = self._load_indicators(stock)

        df = self._merge(prices, indicators)

        df = self._create_lag_features(df)
        df = self._create_return_features(df)
        df = self._create_volatility_features(df)
        df = self._create_target(df)

        df = df.dropna().reset_index(drop=True)

        return df

    def build_latest_features(self, stock):

        df = self.build_dataset(stock)

        if df.empty:
            return None

        return df.iloc[[-1]]

    def _load_prices(self, stock):

        prices = self.stock_repository.get_price_history(stock.id)

        rows = []

        for price in prices:
            rows.append({
                "timestamp": price.timestamp,
                "open": price.open,
                "high": price.high,
                "low": price.low,
                "close": price.close,
                "volume": price.volume
            })

        return pd.DataFrame(rows)

    def _load_indicators(self, stock):

        indicators = self.indicator_repository.get_by_stock(stock.id)

        rows = []

        for indicator in indicators:
            rows.append({
                "timestamp": indicator.timestamp,

                "sma_20": indicator.sma_20,
                "sma_50": indicator.sma_50,
                "sma_200": indicator.sma_200,

                "ema_12": indicator.ema_12,
                "ema_26": indicator.ema_26,

                "rsi_14": indicator.rsi_14,

                "macd": indicator.macd,
                "macd_signal": indicator.macd_signal,
                "macd_histogram": indicator.macd_histogram,

                "bb_upper": indicator.bb_upper,
                "bb_middle": indicator.bb_middle,
                "bb_lower": indicator.bb_lower,

                "atr_14": indicator.atr_14,

                "plus_di_14": indicator.plus_di_14,
                "minus_di_14": indicator.minus_di_14,
                "dx_14": indicator.dx_14,
                "adx_14": indicator.adx_14
            })

        return pd.DataFrame(rows)

    def _merge(self, prices, indicators):

        if prices.empty or indicators.empty:
            return pd.DataFrame()

        df = pd.merge(
            prices,
            indicators,
            on="timestamp",
            how="inner"
        )

        df = df.sort_values("timestamp")
        df.reset_index(drop=True, inplace=True)

        return df

    def _create_lag_features(self, df):

        df["close_lag_1"] = df["close"].shift(1)
        df["close_lag_2"] = df["close"].shift(2)
        df["close_lag_3"] = df["close"].shift(3)
        df["close_lag_5"] = df["close"].shift(5)
        df["close_lag_10"] = df["close"].shift(10)

        df["volume_lag_1"] = df["volume"].shift(1)
        df["volume_lag_5"] = df["volume"].shift(5)

        return df

    def _create_return_features(self, df):

        df["return_1d"] = df["close"].pct_change()

        df["return_5d"] = (
            df["close"] / df["close"].shift(5)
        ) - 1

        df["return_10d"] = (
            df["close"] / df["close"].shift(10)
        ) - 1

        return df

    def _create_volatility_features(self, df):

        daily_returns = df["close"].pct_change()

        df["volatility_5"] = daily_returns.rolling(5).std()
        df["volatility_10"] = daily_returns.rolling(10).std()
        df["volatility_20"] = daily_returns.rolling(20).std()

        return df

    def _create_target(self, df):

        df["target"] = df["close"].shift(-1)

        return df