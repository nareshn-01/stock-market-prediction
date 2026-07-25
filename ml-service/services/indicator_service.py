import pandas as pd
import numpy as np

from models.technical_indicator import TechnicalIndicator
from repositories.stock_repository import StockRepository
from repositories.technical_indicator_repository import (
    TechnicalIndicatorRepository
)


class IndicatorService:

    def __init__(
        self,
        stock_repository: StockRepository,
        indicator_repository: TechnicalIndicatorRepository
    ):
        self.stock_repository = stock_repository
        self.indicator_repository = indicator_repository

    def _update_indicator(self, indicator, row):

        field_mapping = {
            "sma_20": "sma_20",
            "sma_50": "sma_50",
            "sma_200": "sma_200",

            "ema_12": "ema_12",
            "ema_26": "ema_26",

            "rsi_14": "rsi_14",

            "macd": "macd",
            "macd_signal": "macd_signal",
            "macd_histogram": "macd_histogram",

            "bb_upper": "bb_upper",
            "bb_middle": "bb_middle",
            "bb_lower": "bb_lower",

            "atr_14": "atr_14",

            "plus_di": "plus_di_14",
            "minus_di": "minus_di_14",
            "dx": "dx_14",
            "adx": "adx_14"
        }

        for df_column, model_field in field_mapping.items():

            value = row.get(df_column)

            if pd.isna(value):
                setattr(indicator, model_field, None)
            else:
                setattr(indicator, model_field, float(value))

    def calculate_indicators(self, stock):

        prices = self.stock_repository.get_price_history(stock.id)

        if len(prices) < 20:
            return {
                "symbol": stock.symbol,
                "message": "Not enough historical data"
            }

        df = pd.DataFrame([
            {
                "timestamp": price.timestamp,
                "open": float(price.open),
                "high": float(price.high),
                "low": float(price.low),
                "close": float(price.close)
            }
            for price in prices
        ])

        df.sort_values("timestamp", inplace=True)
        df.reset_index(drop=True, inplace=True)

        # ======================================================
        # SMA
        # ======================================================

        df["sma_20"] = df["close"].rolling(window=20).mean()
        df["sma_50"] = df["close"].rolling(window=50).mean()
        df["sma_200"] = df["close"].rolling(window=200).mean()

        # ======================================================
        # EMA
        # ======================================================

        df["ema_12"] = df["close"].ewm(
            span=12,
            adjust=False
        ).mean()

        df["ema_26"] = df["close"].ewm(
            span=26,
            adjust=False
        ).mean()

        # ======================================================
        # MACD
        # ======================================================

        df["macd"] = (
            df["ema_12"] -
            df["ema_26"]
        )

        df["macd_signal"] = (
            df["macd"]
            .ewm(
                span=9,
                adjust=False
            )
            .mean()
        )

        df["macd_histogram"] = (
            df["macd"] -
            df["macd_signal"]
        )

        # ======================================================
        # RSI (14)
        # ======================================================

        delta = df["close"].diff()

        gain = delta.clip(lower=0)

        loss = (-delta).clip(lower=0)

        avg_gain = gain.rolling(window=14).mean()

        avg_loss = loss.rolling(window=14).mean()

        rs = avg_gain / avg_loss

        df["rsi_14"] = 100 - (
            100 / (1 + rs)
        )

        # ======================================================
        # Bollinger Bands (20)
        # ======================================================

        df["bb_middle"] = (
            df["close"]
            .rolling(window=20)
            .mean()
        )

        rolling_std = (
            df["close"]
            .rolling(window=20)
            .std()
        )

        df["bb_upper"] = (
            df["bb_middle"] +
            (2 * rolling_std)
        )

        df["bb_lower"] = (
            df["bb_middle"] -
            (2 * rolling_std)
        )

        # ======================================================
        # ATR (14)
        # ======================================================

        previous_close = df["close"].shift(1)

        tr1 = (
            df["high"] -
            df["low"]
        )

        tr2 = (
            df["high"] -
            previous_close
        ).abs()

        tr3 = (
            df["low"] -
            previous_close
        ).abs()

        df["true_range"] = pd.concat(
            [tr1, tr2, tr3],
            axis=1
        ).max(axis=1)

        df["atr_14"] = (
            df["true_range"]
            .ewm(
                alpha=1/14,
                adjust=False
            )
            .mean()
        )

        # ======================================================
        # Directional Movement
        # ======================================================

        up_move = df["high"].diff()

        down_move = -df["low"].diff()

        plus_dm = up_move.where(
            (
                (up_move > down_move) &
                (up_move > 0)
            ),
            0.0
        )

        minus_dm = down_move.where(
            (
                (down_move > up_move) &
                (down_move > 0)
            ),
            0.0
        )

        # ======================================================
        # +DI / -DI
        # ======================================================

        plus_dm_14 = (
            plus_dm
            .ewm(
                alpha=1/14,
                adjust=False
            )
            .mean()
        )

        minus_dm_14 = (
            minus_dm
            .ewm(
                alpha=1/14,
                adjust=False
            )
            .mean()
        )

        df["plus_di"] = (
            100 *
            plus_dm_14 /
            df["atr_14"]
        )

        df["minus_di"] = (
            100 *
            minus_dm_14 /
            df["atr_14"]
        )

        # ======================================================
        # DX
        # ======================================================

        di_sum = (
            df["plus_di"] +
            df["minus_di"]
        )

        di_sum = di_sum.replace(0, np.nan)

        df["dx"] = (
    (
        (
            df["plus_di"] -
            df["minus_di"]
        ).abs()
        /
        di_sum
    )
    * 100
)

        # ======================================================
        # ADX (Simple Rolling)
        # ======================================================
        df["dx"] = pd.to_numeric(df["dx"], errors="coerce")
        df["adx"] = (
            df["dx"]
            .ewm(
                alpha=1/14,
                adjust=False
            )
            .mean()
        )

        df.drop(
            columns=[
                "true_range"
            ],
            inplace=True,
            errors="ignore"
        )

        inserted = 0
        updated = 0

        new_indicators = []
        for _, row in df.iterrows():

            indicator = self.indicator_repository.get_by_stock_timestamp(
                stock.id,
                row["timestamp"]
            )

            if indicator is not None:

                self._update_indicator(
                    indicator,
                    row
                )

                updated += 1

            else:

                indicator = TechnicalIndicator(
                    stock_id=stock.id,
                    timestamp=row["timestamp"],
                    interval="1d"
                )

                self._update_indicator(
                    indicator,
                    row
                )

                new_indicators.append(indicator)

                inserted += 1

        if new_indicators:
            self.indicator_repository.save_all(
                new_indicators
            )

        self.indicator_repository.commit()

        return {
            "symbol": stock.symbol,
            "records_processed": len(df),
            "records_inserted": inserted,
            "records_updated": updated
        }