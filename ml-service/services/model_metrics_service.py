from repositories.model_metrics_repository import ModelMetricsRepository


class ModelMetricsService:

    def __init__(self, repository: ModelMetricsRepository):
        self.repository = repository

    def save(self, metrics):
        return self.repository.save(metrics)

    def get_latest(self, symbol: str):
        return self.repository.get_latest(symbol)

    def get_all(self):
        return self.repository.get_all()

    def get_by_symbol(self, symbol: str):
        return self.repository.get_by_symbol(symbol)

    def delete(self, symbol: str):
        return self.repository.delete(symbol)

    def count(self):
        return self.repository.count()