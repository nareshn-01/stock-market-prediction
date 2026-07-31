from pathlib import Path
from typing import Any, List

import joblib


class ModelLoader:
    """
    Utility class for saving, loading and managing trained ML models.
    """

    MODEL_DIR = Path("saved_models")

    @classmethod
    def _ensure_directory(cls):
        cls.MODEL_DIR.mkdir(parents=True, exist_ok=True)

    @classmethod
    def _normalize(cls, value: str) -> str:
        return value.strip().upper()

    @classmethod
    def get_model_path(
        cls,
        symbol: str,
        model_name: str
    ) -> Path:

        cls._ensure_directory()

        symbol = cls._normalize(symbol)
        model_name = cls._normalize(model_name)

        return cls.MODEL_DIR / f"{symbol}_{model_name}.pkl"

    @classmethod
    def save_model(
        cls,
        symbol: str,
        model: Any,
        model_name: str
    ) -> str:

        if model is None:
            raise ValueError("Cannot save an empty model.")

        path = cls.get_model_path(
            symbol,
            model_name
        )

        joblib.dump(model, path)

        return str(path)

    @classmethod
    def load_model(
        cls,
        symbol: str,
        model_name: str
    ) -> Any:

        path = cls.get_model_path(
            symbol,
            model_name
        )

        if not path.exists():
            raise FileNotFoundError(
                f"Model '{model_name}' for '{symbol}' does not exist."
            )

        return joblib.load(path)

    @classmethod
    def model_exists(
        cls,
        symbol: str,
        model_name: str
    ) -> bool:

        return cls.get_model_path(
            symbol,
            model_name
        ).exists()

    @classmethod
    def delete_model(
        cls,
        symbol: str,
        model_name: str
    ) -> bool:

        path = cls.get_model_path(
            symbol,
            model_name
        )

        if path.exists():
            path.unlink()
            return True

        return False

    @classmethod
    def delete_all_models(
        cls,
        symbol: str
    ) -> int:

        cls._ensure_directory()

        symbol = cls._normalize(symbol)

        deleted = 0

        for file in cls.MODEL_DIR.glob(f"{symbol}_*.pkl"):
            file.unlink()
            deleted += 1

        return deleted

    @classmethod
    def list_models(cls) -> List[str]:

        cls._ensure_directory()

        return sorted(
            file.stem
            for file in cls.MODEL_DIR.glob("*.pkl")
        )

    @classmethod
    def list_models_for_symbol(
        cls,
        symbol: str
    ) -> List[str]:

        cls._ensure_directory()

        symbol = cls._normalize(symbol)

        return sorted(
            file.stem
            for file in cls.MODEL_DIR.glob(f"{symbol}_*.pkl")
        )

    @classmethod
    def get_model_count(cls) -> int:

        cls._ensure_directory()

        return len(list(cls.MODEL_DIR.glob("*.pkl")))