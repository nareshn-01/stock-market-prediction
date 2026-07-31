import numpy as np
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

        if df.empty:
            return df

        df = self._convert_numeric_columns(df)

        df = self._create_lag_features(df)
        df = self._create_return_features(df)
        df = self._create_volatility_features(df)
        df = self._create_price_features(df)
        df = self._create_indicator_features(df)
        df = self._create_target(df)

        df = self._convert_numeric_columns(df)

        df = (
            df
            .replace([np.inf, -np.inf], np.nan)
            .drop_duplicates(subset=["timestamp"])
            .dropna()
            .reset_index(drop=True)
        )

        return df

    def build_latest_features(self, stock):

        df = self.build_dataset(stock)

        if df.empty:
            return None

        return df.tail(1)

    def _load_prices(self, stock):

        prices = self.stock_repository.get_price_history(stock.id)

        rows = []

        for price in prices:

            rows.append({
                "timestamp": price.timestamp,

                "open": float(price.open)
                if price.open is not None else None,

                "high": float(price.high)
                if price.high is not None else None,

                "low": float(price.low)
                if price.low is not None else None,

                "close": float(price.close)
                if price.close is not None else None,

                "volume": int(price.volume)
                if price.volume is not None else None
            })

        return pd.DataFrame(rows)

    def _load_indicators(self, stock):

        indicators = self.indicator_repository.get_by_stock(
            stock.id
        )

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

        return (
            df
            .sort_values("timestamp")
            .reset_index(drop=True)
        )

    def _convert_numeric_columns(self, df):

        numeric_columns = [
            c
            for c in df.columns
            if c != "timestamp"
        ]

        df[numeric_columns] = df[numeric_columns].apply(
            pd.to_numeric,
            errors="coerce"
        )

        return df

    def _create_lag_features(self, df):

        for lag in [1, 2, 3, 5, 10]:
            df[f"close_lag_{lag}"] = df["close"].shift(lag)

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

        df["log_return"] = np.log(
            df["close"] / df["close"].shift(1)
        )

        return df

    def _create_volatility_features(self, df):

        returns = df["close"].pct_change()

        df["volatility_5"] = returns.rolling(5).std()

        df["volatility_10"] = returns.rolling(10).std()

        df["volatility_20"] = returns.rolling(20).std()

        return df

    def _create_price_features(self, df):

        df["price_range"] = (
            df["high"] - df["low"]
        )

        df["high_low_pct"] = (
            (df["high"] - df["low"])
            / df["close"]
        )

        df["open_close_pct"] = (
            (df["close"] - df["open"])
            / df["open"]
        )

        df["momentum_5"] = (
            df["close"] - df["close"].shift(5)
        )

        df["momentum_10"] = (
            df["close"] - df["close"].shift(10)
        )

        df["volume_change"] = (
            df["volume"].pct_change()
        )

        return df

    def _create_indicator_features(self, df):

        df["sma_spread"] = (
            df["sma_20"] - df["sma_50"]
        )

        df["ema_spread"] = (
            df["ema_12"] - df["ema_26"]
        )

        df["macd_diff"] = (
            df["macd"] - df["macd_signal"]
        )

        df["bb_width"] = (
            df["bb_upper"] - df["bb_lower"]
        )

        df["atr_percent"] = (
            df["atr_14"] / df["close"]
        )

        return df

    def _create_target(self, df):

        df["target"] = (
            df["close"].shift(-1)
        )

        return df