from repositories.prediction_repository import PredictionRepository


class PredictionHistoryService:

    def __init__(self, prediction_repository: PredictionRepository):
        self.prediction_repository = prediction_repository

    def get_history(self, symbol: str, limit: int = 100):
        return self.prediction_repository.get_history(symbol, limit)

    def get_latest(self, symbol: str):
        return self.prediction_repository.get_latest(symbol)

    def delete_history(self, symbol: str):
        deleted = self.prediction_repository.delete_history(symbol)

        return {
            "symbol": symbol.upper(),
            "deleted_records": deleted
        }

    def count(self, symbol: str):
        return self.prediction_repository.count(symbol)