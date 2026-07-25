import os
import joblib
from typing import Any, List


class ModelLoader:
    """
    Utility class for managing trained ML models.
    """

    MODEL_DIR = "saved_models"

    @classmethod
    def _ensure_directory(cls):
        """
        Create model directory if it doesn't exist.
        """
        os.makedirs(cls.MODEL_DIR, exist_ok=True)

    @classmethod
    def get_model_path(cls, symbol: str) -> str:
        """
        Returns the model file path.
        """
        cls._ensure_directory()
        return os.path.join(cls.MODEL_DIR, f"{symbol.upper()}.pkl")

    @classmethod
    def save_model(cls, symbol: str, model: Any) -> str:
        """
        Save trained model.
        """
        path = cls.get_model_path(symbol)

        joblib.dump(model, path)

        return path

    @classmethod
    def load_model(cls, symbol: str) -> Any:
        """
        Load trained model.
        """
        path = cls.get_model_path(symbol)

        if not os.path.exists(path):
            raise FileNotFoundError(
                f"Model not found for symbol: {symbol}"
            )

        return joblib.load(path)

    @classmethod
    def model_exists(cls, symbol: str) -> bool:
        """
        Check whether model exists.
        """
        path = cls.get_model_path(symbol)

        return os.path.exists(path)

    @classmethod
    def delete_model(cls, symbol: str):
        """
        Delete a trained model.
        """
        path = cls.get_model_path(symbol)

        if os.path.exists(path):
            os.remove(path)

    @classmethod
    def list_models(cls) -> List[str]:
        """
        List all trained models.
        """
        cls._ensure_directory()

        models = []

        for file in os.listdir(cls.MODEL_DIR):
            if file.endswith(".pkl"):
                models.append(file.replace(".pkl", ""))

        return sorted(models)