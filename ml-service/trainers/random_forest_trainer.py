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
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42,
            n_jobs=-1
        )

        self.best_params = self.model.get_params()

    def train(
        self,
        X_train,
        y_train,
        tune=False
    ):
        """
        Train Random Forest.

        tune=False -> Fast training
        tune=True  -> Hyperparameter tuning
        """

        if tune:

            param_grid = {
                "n_estimators": [100, 200, 300],
                "max_depth": [5, 10, 15, None],
                "min_samples_split": [2, 5, 10],
                "min_samples_leaf": [1, 2, 4],
                "max_features": ["sqrt", "log2"]
            }

            self.model, self.best_params = HyperparameterService.tune(
                model=self.model,
                param_grid=param_grid,
                X_train=X_train,
                y_train=y_train,
                n_iter=10,
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
        return ModelType.RANDOM_FOREST.value

    @property
    def version(self):
        return "v1.1"

    @property
    def estimator(self):
        return self.model

    @property
    def parameters(self):
        return self.best_params