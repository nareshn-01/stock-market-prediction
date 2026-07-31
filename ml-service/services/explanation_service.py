class ExplanationService:

    """
    Generates explainable AI reasons.
    """

    @staticmethod
    def generate(
        latest_features
    ):

        reasons = []

        row = latest_features.iloc[0]

        # RSI

        if row["rsi_14"] < 30:
            reasons.append(
                "RSI indicates oversold conditions."
            )

        elif row["rsi_14"] > 70:
            reasons.append(
                "RSI indicates overbought conditions."
            )

        else:
            reasons.append(
                "RSI is in a healthy range."
            )

        # MACD

        if row["macd"] > row["macd_signal"]:
            reasons.append(
                "MACD bullish crossover detected."
            )

        else:
            reasons.append(
                "MACD bearish crossover detected."
            )

        # EMA

        if row["ema_12"] > row["ema_26"]:
            reasons.append(
                "Short-term EMA is above long-term EMA."
            )

        else:
            reasons.append(
                "Short-term EMA is below long-term EMA."
            )

        # ADX

        if row["adx_14"] >= 25:
            reasons.append(
                "ADX indicates a strong trend."
            )

        else:
            reasons.append(
                "ADX indicates a weak trend."
            )

        return reasons