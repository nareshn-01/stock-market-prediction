from catboost import CatBoostRegressor

from models.model_type import ModelType
from services.hyperparameter_service import HyperparameterService
from trainers.base_trainer import BaseTrainer
from utils.model_loader import ModelLoader


class CatBoostTrainer(BaseTrainer):

    def __init__(self):

        self.model = CatBoostRegressor(
            iterations=300,
            depth=6,
            learning_rate=0.05,
            l2_leaf_reg=3,
            random_seed=42,
            verbose=False
        )

        self.best_params = self.model.get_params()

    def train(
        self,
        X_train,
        y_train,
        tune=False
    ):
        """
        Train CatBoost.

        tune=False -> Fast training
        tune=True  -> Hyperparameter tuning
        """

        if tune:

            param_grid = {
                "iterations": [200, 300],
                "depth": [4, 6],
                "learning_rate": [0.03, 0.05],
                "l2_leaf_reg": [3, 5]
            }

            self.model, self.best_params = HyperparameterService.tune(
                model=self.model,
                param_grid=param_grid,
                X_train=X_train,
                y_train=y_train,
                n_iter=6,
                cv=3
            )

        else:

            self.model.fit(
                X_train,
                y_train
            )

            self.best_params = self.model.get_params()

    def predict(
        self,
        X_test
    ):
        return self.model.predict(X_test)

    def save(
        self,
        symbol: str
    ):
        return ModelLoader.save_model(
            symbol,
            self.model,
            self.model_name
        )

    @property
    def model_name(self):
        return ModelType.CATBOOST.value

    @property
    def version(self):
        return "v1.1"

    @property
    def estimator(self):
        return self.model

    @property
    def parameters(self):
        return self.best_params