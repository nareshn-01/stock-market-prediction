import pandas as pd

from models.prediction import Prediction
from models.prediction_history import PredictionHistory

from repositories.prediction_repository import PredictionRepository
from repositories.model_metrics_repository import (
    ModelMetricsRepository
)

from services.feature_engineering_service import (
    FeatureEngineeringService
)
from services.confidence_service import ConfidenceService
from services.recommendation_service import (
    RecommendationService
)
from services.explanation_service import (
    ExplanationService
)

from utils.model_loader import ModelLoader


class PredictionService:

    def __init__(
        self,
        feature_service: FeatureEngineeringService,
        prediction_repository: PredictionRepository,
        metrics_repository: ModelMetricsRepository
    ):
        self.feature_service = feature_service
        self.prediction_repository = prediction_repository
        self.metrics_repository = metrics_repository

    def predict(
        self,
        stock,
        model_name: str
    ) -> Prediction:
        """
        Predict the next closing price using a trained model.
        """

        if not ModelLoader.model_exists(
            stock.symbol,
            model_name
        ):
            raise FileNotFoundError(
                f"{model_name} model not found for {stock.symbol}. "
                "Train the model before prediction."
            )

        model = ModelLoader.load_model(
            stock.symbol,
            model_name
        )

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
            ],
            errors="ignore"
        )

        X = X.apply(
            pd.to_numeric,
            errors="coerce"
        )

        X = X.dropna()

        if X.empty:
            raise ValueError(
                "Latest feature row contains invalid values."
            )

        predicted_price = float(
            model.predict(X)[0]
        )

        current_price = float(
            latest.iloc[0]["close"]
        )

        change_percent = (
            (predicted_price - current_price)
            / current_price
        ) * 100

        # -----------------------------------------
        # Model evaluation metrics
        # -----------------------------------------

        metrics = self.metrics_repository.get_latest(
            stock.symbol,
            model_name
        )

        confidence = ConfidenceService.calculate(
            metrics,
            latest
        )

        signal = RecommendationService.generate(
            change_percent,
            confidence
        )

        reasons = ExplanationService.generate(
            latest
        )

        if confidence >= 85:
            risk = "LOW"

        elif confidence >= 70:
            risk = "MEDIUM"

        else:
            risk = "HIGH"

        prediction = Prediction(
            symbol=stock.symbol,
            current_price=round(current_price, 2),
            predicted_price=round(predicted_price, 2),
            change_percent=round(change_percent, 2),
            signal=signal,
            model=model_name,
            confidence=confidence,
            risk=risk,
            reasons=reasons
        )

        history = PredictionHistory(
            symbol=prediction.symbol,
            current_price=prediction.current_price,
            predicted_price=prediction.predicted_price,
            change_percent=prediction.change_percent,
            signal=prediction.signal
        )

        self.prediction_repository.save(
            history
        )

        return prediction