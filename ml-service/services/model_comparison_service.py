from models.model_type import ModelType
from services.training_service import TrainingService


class ModelComparisonService:

    def __init__(
        self,
        training_service: TrainingService
    ):
        self.training_service = training_service

    def compare(
        self,
        stock,
        tune: bool = False
    ):
        """
        Train and compare all supported ML models.

        Parameters
        ----------
        tune : bool
            False -> Fast training
            True  -> Hyperparameter tuning
        """

        results = []

        models = [
            ModelType.RANDOM_FOREST,
            ModelType.XGBOOST,
            ModelType.LIGHTGBM,
            ModelType.CATBOOST
        ]

        for model_type in models:

            trained_model = self.training_service.train(
                stock=stock,
                model_type=model_type,
                tune=tune
            )

            results.append(trained_model)

        results.sort(
            key=lambda model: model.rmse
        )

        best_model = results[0]

        return {
            "best_model": best_model.algorithm,
            "best_rmse": best_model.rmse,
            "best_r2": best_model.r2,
            "results": results
        }