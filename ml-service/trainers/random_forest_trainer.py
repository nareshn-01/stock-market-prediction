from sklearn.ensemble import RandomForestRegressor

from models.model_type import ModelType
from services.hyperparameter_service import HyperparameterService
from trainers.base_trainer import BaseTrainer
from utils.model_loader import ModelLoader


class RandomForestTrainer(BaseTrainer):

    def __init__(self):

        self.model = RandomForestRegressor(
            n_estimators=200,
            max_depth=10,
            random_state=42,
            n_jobs=-1
        )

        self.best_params = {}

    def train(
        self,
        X_train,
        y_train
    ):
        """
        Train Random Forest using GridSearchCV.
        """

        param_grid = {
            "n_estimators": [100, 200, 300],
            "max_depth": [5, 10, 15],
            "min_samples_split": [2, 5],
            "min_samples_leaf": [1, 2]
        }

        self.model, self.best_params = HyperparameterService.tune(
            self.model,
            param_grid,
            X_train,
            y_train
        )

    def predict(
        self,
        X_test
    ):
        return self.model.predict(
            X_test
        )

    def save(
        self,
        symbol: str
    ):
        return ModelLoader.save_model(
            symbol,
            self.model
        )

    @property
    def model_name(self):
        return ModelType.RANDOM_FOREST.value

    @property
    def version(self):
        return "v1.0"

    @property
    def estimator(self):
        return self.model

    @property
    def parameters(self):
        return self.best_params