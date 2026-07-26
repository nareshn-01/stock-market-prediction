from models.model_type import ModelType
from trainers.random_forest_trainer import RandomForestTrainer
from trainers.xgboost_trainer import XGBoostTrainer


class TrainerFactory:

    @staticmethod
    def get_trainer(model_type: ModelType):

        if model_type == ModelType.RANDOM_FOREST:
            return RandomForestTrainer()

        if model_type == ModelType.XGBOOST:
            return XGBoostTrainer()

        raise ValueError(
            f"Unsupported model type: {model_type}"
        )