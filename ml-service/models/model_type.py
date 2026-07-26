from enum import Enum


class ModelType(str, Enum):
    RANDOM_FOREST = "RandomForest"
    XGBOOST = "XGBoost"
    LIGHTGBM = "LightGBM"
    CATBOOST = "CatBoost"