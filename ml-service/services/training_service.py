from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)
from sklearn.model_selection import train_test_split

from models.trained_model import TrainedModel
from services.feature_engineering_service import (
    FeatureEngineeringService
)
from utils.model_loader import ModelLoader


class TrainingService:

    def __init__(
        self,
        feature_service: FeatureEngineeringService
    ):
        self.feature_service = feature_service

    def train(self, stock) -> TrainedModel:
        """
        Train a Random Forest model for the given stock.
        """

        df = self.feature_service.build_dataset(stock)

        if df.empty:
            raise ValueError(
                f"No training data found for {stock.symbol}"
            )

        X = df.drop(
            columns=[
                "timestamp",
                "target"
            ]
        )

        y = df["target"]

        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=0.2,
            shuffle=False,
            random_state=42
        )

        model = RandomForestRegressor(
            n_estimators=200,
            max_depth=10,
            random_state=42,
            n_jobs=-1
        )

        model.fit(
            X_train,
            y_train
        )

        predictions = model.predict(X_test)

        mae = mean_absolute_error(
            y_test,
            predictions
        )

        rmse = (
            mean_squared_error(
                y_test,
                predictions
            ) ** 0.5
        )

        r2 = r2_score(
            y_test,
            predictions
        )

        model_path = ModelLoader.save_model(
            stock.symbol,
            model
        )

        return TrainedModel(
            symbol=stock.symbol,
            algorithm="Random Forest",
            model_path=model_path,
            samples=len(df),
            train_samples=len(X_train),
            test_samples=len(X_test),
            mae=round(mae, 4),
            rmse=round(rmse, 4),
            r2=round(r2, 4)
        )