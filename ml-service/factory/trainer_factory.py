from models.model_type import ModelType
from trainers.catboost_trainer import CatBoostTrainer
from trainers.lightgbm_trainer import LightGBMTrainer
from trainers.random_forest_trainer import RandomForestTrainer
from trainers.xgboost_trainer import XGBoostTrainer


class TrainerFactory:

    _TRAINERS = {
        ModelType.RANDOM_FOREST: RandomForestTrainer,
        ModelType.XGBOOST: XGBoostTrainer,
        ModelType.LIGHTGBM: LightGBMTrainer,
        ModelType.CATBOOST: CatBoostTrainer,
    }

    @staticmethod
    def get_trainer(model_type: ModelType):

        trainer_class = TrainerFactory._TRAINERS.get(model_type)

        if trainer_class is None:
            supported = ", ".join(
                model.value
                for model in TrainerFactory._TRAINERS.keys()
            )

            raise ValueError(
                f"Unsupported model type: {model_type}. "
                f"Supported models: {supported}"
            )

        return trainer_class()