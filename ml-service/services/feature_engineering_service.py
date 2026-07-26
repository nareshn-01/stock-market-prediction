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

        # Convert all database values to numeric
        df = self._convert_numeric_columns(df)

        df = self._create_lag_features(df)
        df = self._create_return_features(df)
        df = self._create_volatility_features(df)
        df = self._create_target(df)

        # Convert newly created columns too
        df = self._convert_numeric_columns(df)

        df = (
            df
            .dropna()
            .reset_index(drop=True)
        )

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

                "open": float(price.open) if price.open is not None else None,
                "high": float(price.high) if price.high is not None else None,
                "low": float(price.low) if price.low is not None else None,
                "close": float(price.close) if price.close is not None else None,

                "volume": int(price.volume) if price.volume is not None else None
            })

        return pd.DataFrame(rows)

    def _load_indicators(self, stock):

        indicators = self.indicator_repository.get_by_stock(stock.id)

        rows = []

        for indicator in indicators:

            rows.append({

                "timestamp": indicator.timestamp,

                "sma_20": float(indicator.sma_20) if indicator.sma_20 is not None else None,
                "sma_50": float(indicator.sma_50) if indicator.sma_50 is not None else None,
                "sma_200": float(indicator.sma_200) if indicator.sma_200 is not None else None,

                "ema_12": float(indicator.ema_12) if indicator.ema_12 is not None else None,
                "ema_26": float(indicator.ema_26) if indicator.ema_26 is not None else None,

                "rsi_14": float(indicator.rsi_14) if indicator.rsi_14 is not None else None,

                "macd": float(indicator.macd) if indicator.macd is not None else None,
                "macd_signal": float(indicator.macd_signal) if indicator.macd_signal is not None else None,
                "macd_histogram": float(indicator.macd_histogram) if indicator.macd_histogram is not None else None,

                "bb_upper": float(indicator.bb_upper) if indicator.bb_upper is not None else None,
                "bb_middle": float(indicator.bb_middle) if indicator.bb_middle is not None else None,
                "bb_lower": float(indicator.bb_lower) if indicator.bb_lower is not None else None,

                "atr_14": float(indicator.atr_14) if indicator.atr_14 is not None else None,

                "plus_di_14": float(indicator.plus_di_14) if indicator.plus_di_14 is not None else None,
                "minus_di_14": float(indicator.minus_di_14) if indicator.minus_di_14 is not None else None,
                "dx_14": float(indicator.dx_14) if indicator.dx_14 is not None else None,
                "adx_14": float(indicator.adx_14) if indicator.adx_14 is not None else None
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

    def _convert_numeric_columns(self, df):

        numeric_columns = [
            column
            for column in df.columns
            if column != "timestamp"
        ]

        for column in numeric_columns:
            df[column] = pd.to_numeric(
                df[column],
                errors="coerce"
            )

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