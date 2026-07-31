from models.model_metrics import ModelMetrics


class ConfidenceService:
    """
    Calculates prediction confidence using
    model evaluation metrics and technical indicators.
    """

    @staticmethod
    def calculate(
        metrics: ModelMetrics,
        latest_features
    ) -> float:

        confidence = 50.0

        # -----------------------------------
        # Model Performance
        # -----------------------------------

        confidence += metrics.r2_score * 30

        confidence -= metrics.rmse / 50

        # -----------------------------------
        # RSI
        # -----------------------------------

        rsi = latest_features.iloc[0]["rsi_14"]

        if 40 <= rsi <= 60:
            confidence += 8

        elif 30 <= rsi < 40:
            confidence += 5

        elif 60 < rsi <= 70:
            confidence += 5

        # -----------------------------------
        # ADX
        # -----------------------------------

        adx = latest_features.iloc[0]["adx_14"]

        if adx >= 30:
            confidence += 10

        elif adx >= 20:
            confidence += 5

        # -----------------------------------
        # MACD
        # -----------------------------------

        macd = latest_features.iloc[0]["macd"]

        signal = latest_features.iloc[0]["macd_signal"]

        if macd > signal:
            confidence += 5

        else:
            confidence -= 5

        # -----------------------------------
        # EMA Trend
        # -----------------------------------

        ema12 = latest_features.iloc[0]["ema_12"]

        ema26 = latest_features.iloc[0]["ema_26"]

        if ema12 > ema26:
            confidence += 7

        else:
            confidence -= 7

        confidence = max(
            0,
            min(100, confidence)
        )

        return round(confidence, 2)