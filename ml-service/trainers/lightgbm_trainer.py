from lightgbm import LGBMRegressor

from models.model_type import ModelType
from services.hyperparameter_service import HyperparameterService
from trainers.base_trainer import BaseTrainer
from utils.model_loader import ModelLoader


class LightGBMTrainer(BaseTrainer):

    def __init__(self):

        self.model = LGBMRegressor(
            n_estimators=300,
            learning_rate=0.05,
            max_depth=6,
            num_leaves=31,
            subsample=0.8,
            colsample_bytree=0.8,
            random_state=42,
            n_jobs=-1,
            verbosity=-1
        )

        self.best_params = self.model.get_params()

    def train(
        self,
        X_train,
        y_train,
        tune=False
    ):
        """
        Train LightGBM.

        tune=False -> Fast training
        tune=True  -> Hyperparameter tuning
        """

        if tune:

            param_grid = {
                "n_estimators": [200, 300, 500],
                "learning_rate": [0.03, 0.05, 0.1],
                "max_depth": [4, 6, 8],
                "num_leaves": [31, 63, 127],
                "subsample": [0.8, 1.0],
                "colsample_bytree": [0.8, 1.0]
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
        return ModelType.LIGHTGBM.value

    @property
    def version(self):
        return "v1.1"

    @property
    def estimator(self):
        return self.model

    @property
    def parameters(self):
        return self.best_params