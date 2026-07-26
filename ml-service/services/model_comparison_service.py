from models.model_type import ModelType
from services.training_service import TrainingService


class ModelComparisonService:

    def __init__(self, training_service: TrainingService):
        self.training_service = training_service

    def compare(self, stock):

        results = []

        for model_type in [
            ModelType.RANDOM_FOREST,
            ModelType.XGBOOST
        ]:

            model = self.training_service.train(
                stock,
                model_type
            )

            results.append(model)

        best_model = min(
            results,
            key=lambda x: x.rmse
        )

        return {
            "best_model": best_model.algorithm,
            "results": results
        }