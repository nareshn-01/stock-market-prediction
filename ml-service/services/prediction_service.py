from models.prediction import Prediction
from models.prediction_history import PredictionHistory
from repositories.prediction_repository import PredictionRepository
from services.feature_engineering_service import (
    FeatureEngineeringService
)
from utils.model_loader import ModelLoader


class PredictionService:

    def __init__(
        self,
        feature_service: FeatureEngineeringService,
        prediction_repository: PredictionRepository
    ):
        self.feature_service = feature_service
        self.prediction_repository = prediction_repository

    def predict(self, stock) -> Prediction:
        """
        Predict the next closing price for the given stock.
        """

        if not ModelLoader.model_exists(stock.symbol):
            raise FileNotFoundError(
                f"Model not found for {stock.symbol}"
            )

        model = ModelLoader.load_model(stock.symbol)

        latest = self.feature_service.build_latest_features(
            stock
        )

        if latest is None or latest.empty:
            raise ValueError(
                f"No feature data available for {stock.symbol}"
            )

        X = latest.drop(
            columns=[
                "timestamp",
                "target"
            ]
        )

        predicted_price = float(model.predict(X)[0])

        current_price = float(
            latest.iloc[0]["close"]
        )

        change_percent = (
            (predicted_price - current_price)
            / current_price
        ) * 100

        if change_percent >= 2:
            signal = "STRONG BUY"

        elif change_percent >= 0.5:
            signal = "BUY"

        elif change_percent <= -2:
            signal = "STRONG SELL"

        elif change_percent <= -0.5:
            signal = "SELL"

        else:
            signal = "HOLD"

        prediction = Prediction(
            symbol=stock.symbol,
            current_price=round(current_price, 2),
            predicted_price=round(predicted_price, 2),
            change_percent=round(change_percent, 2),
            signal=signal
        )

        history = PredictionHistory(
            symbol=prediction.symbol,
            current_price=prediction.current_price,
            predicted_price=prediction.predicted_price,
            change_percent=prediction.change_percent,
            signal=prediction.signal
        )

        self.prediction_repository.save(history)

        return prediction