class RecommendationService:

    """
    Generates trading recommendation.
    """

    @staticmethod
    def generate(
        expected_return: float,
        confidence: float
    ) -> str:

        if confidence >= 85:

            if expected_return >= 3:
                return "STRONG BUY"

            if expected_return >= 1:
                return "BUY"

            if expected_return <= -3:
                return "STRONG SELL"

            if expected_return <= -1:
                return "SELL"

        if confidence >= 70:

            if expected_return >= 2:
                return "BUY"

            if expected_return <= -2:
                return "SELL"

        return "HOLD"