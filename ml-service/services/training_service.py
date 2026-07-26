import pandas as pd
from sklearn.metrics import (
    mean_absolute_error,
    mean_absolute_percentage_error,
    mean_squared_error,
    r2_score
)
from sklearn.model_selection import train_test_split

from factory.trainer_factory import TrainerFactory
from models.model_metrics import ModelMetrics
from models.model_type import ModelType
from models.trained_model import TrainedModel
from repositories.model_metrics_repository import (
    ModelMetricsRepository
)
from services.feature_engineering_service import (
    FeatureEngineeringService
)


class TrainingService:

    def __init__(
        self,
        feature_service: FeatureEngineeringService,
        metrics_repository: ModelMetricsRepository
    ):
        self.feature_service = feature_service
        self.metrics_repository = metrics_repository

    def train(
        self,
        stock,
        model_type: ModelType = ModelType.RANDOM_FOREST
    ) -> TrainedModel:
        """
        Train the selected model for the given stock.
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

        # Convert all features to numeric
        X = X.apply(pd.to_numeric, errors="coerce")

        # Convert target to numeric
        y = pd.to_numeric(
            df["target"],
            errors="coerce"
        )

        # Remove invalid rows
        valid_rows = X.notna().all(axis=1) & y.notna()

        X = X.loc[valid_rows]
        y = y.loc[valid_rows]

        if X.empty:
            raise ValueError(
                "Dataset contains no valid numeric rows after preprocessing."
            )

        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=0.2,
            shuffle=False,
            random_state=42
        )

        trainer = TrainerFactory.get_trainer(
            model_type
        )

        trainer.train(
            X_train,
            y_train
        )

        predictions = trainer.predict(
            X_test
        )

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

        mape = mean_absolute_percentage_error(
            y_test,
            predictions
        )

        r2 = r2_score(
            y_test,
            predictions
        )

        model_path = trainer.save(
            stock.symbol
        )

        metrics = ModelMetrics(
            symbol=stock.symbol,
            model_name=trainer.model_name,
            model_version=trainer.version,
            mae=round(mae, 4),
            rmse=round(rmse, 4),
            mape=round(mape, 4),
            r2_score=round(r2, 4),
            training_samples=len(X)
        )

        self.metrics_repository.save(metrics)

        return TrainedModel(
            symbol=stock.symbol,
            algorithm=trainer.model_name,
            model_path=model_path,
            samples=len(X),
            train_samples=len(X_train),
            test_samples=len(X_test),
            mae=round(mae, 4),
            rmse=round(rmse, 4),
            r2=round(r2, 4),
            parameters=trainer.parameters
        )