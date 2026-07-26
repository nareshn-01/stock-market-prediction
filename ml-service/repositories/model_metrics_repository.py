from sqlalchemy.orm import Session

from models.model_metrics import ModelMetrics


class ModelMetricsRepository:

    def __init__(self, db: Session):
        self.db = db

    def save(self, metrics: ModelMetrics):
        self.db.add(metrics)
        self.db.commit()
        self.db.refresh(metrics)
        return metrics

    def get_latest(self, symbol: str):
        return (
            self.db.query(ModelMetrics)
            .filter(ModelMetrics.symbol == symbol)
            .order_by(ModelMetrics.trained_at.desc())
            .first()
        )

    def get_all(self):
        return (
            self.db.query(ModelMetrics)
            .order_by(ModelMetrics.trained_at.desc())
            .all()
        )

    def get_by_symbol(self, symbol: str):
        return (
            self.db.query(ModelMetrics)
            .filter(ModelMetrics.symbol == symbol)
            .order_by(ModelMetrics.trained_at.desc())
            .all()
        )

    def delete(self, symbol: str):
        return (
            self.db.query(ModelMetrics)
            .filter(ModelMetrics.symbol == symbol)
            .delete()
        )

    def count(self):
        return self.db.query(ModelMetrics).count()