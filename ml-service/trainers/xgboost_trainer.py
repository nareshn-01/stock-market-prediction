from xgboost import XGBRegressor

from models.model_type import ModelType
from services.hyperparameter_service import HyperparameterService
from trainers.base_trainer import BaseTrainer
from utils.model_loader import ModelLoader


class XGBoostTrainer(BaseTrainer):

    def __init__(
        self,
        n_estimators: int = 300,
        learning_rate: float = 0.05,
        max_depth: int = 6,
        random_state: int = 42
    ):
        self.model = XGBRegressor(
            n_estimators=n_estimators,
            learning_rate=learning_rate,
            max_depth=max_depth,
            random_state=random_state,
            objective="reg:squarederror",
            n_jobs=-1
        )

        self.best_params = {}

    def train(
        self,
        X_train,
        y_train
    ):
        """
        Train the XGBoost model using GridSearchCV.
        """

        param_grid = {
            "n_estimators": [100, 200],
            "learning_rate": [0.01, 0.05, 0.1],
            "max_depth": [3, 5, 7]
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
        """
        Predict using the trained model.
        """
        return self.model.predict(X_test)

    def save(
        self,
        symbol: str
    ) -> str:
        """
        Save the trained model.
        """
        return ModelLoader.save_model(
            f"{symbol}_XGBOOST",
            self.model
        )

    @property
    def model_name(self) -> str:
        return ModelType.XGBOOST.value

    @property
    def version(self) -> str:
        return "v1.0"

    @property
    def estimator(self):
        return self.model

    @property
    def parameters(self):
        return self.best_params