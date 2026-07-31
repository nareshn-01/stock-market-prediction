from sqlalchemy import asc
from sqlalchemy.orm import Session

from models.model_metrics import ModelMetrics


class ModelMetricsRepository:

    def __init__(
        self,
        db: Session
    ):
        self.db = db

    # ---------------------------------------------------------
    # Save
    # ---------------------------------------------------------

    def save(
        self,
        metrics: ModelMetrics
    ) -> ModelMetrics:

        self.db.add(metrics)
        self.db.commit()
        self.db.refresh(metrics)

        return metrics

    # ---------------------------------------------------------
    # Get All Models
    # ---------------------------------------------------------

    def find_all(
        self,
        symbol: str
    ):
        """
        Return all trained models for a stock,
        ordered by RMSE.
        """

        return (
            self.db.query(ModelMetrics)
            .filter(
                ModelMetrics.symbol == symbol
            )
            .order_by(
                asc(ModelMetrics.rmse)
            )
            .all()
        )

    # ---------------------------------------------------------
    # Best Model
    # ---------------------------------------------------------

    def find_best_model(
        self,
        symbol: str
    ):
        """
        Return the model with the lowest RMSE.
        """

        return (
            self.db.query(ModelMetrics)
            .filter(
                ModelMetrics.symbol == symbol
            )
            .order_by(
                asc(ModelMetrics.rmse)
            )
            .first()
        )

    # ---------------------------------------------------------
    # Find By Model
    # ---------------------------------------------------------

    def find_by_model(
        self,
        symbol: str,
        model_name: str
    ):
        """
        Return metrics for a specific model.
        """

        return (
            self.db.query(ModelMetrics)
            .filter(
                ModelMetrics.symbol == symbol,
                ModelMetrics.model_name == model_name
            )
            .first()
        )

    # ---------------------------------------------------------
    # Latest Metrics
    # ---------------------------------------------------------

    def get_latest(
        self,
        symbol: str,
        model_name: str
    ) -> ModelMetrics:
        """
        Return the latest metrics for the given
        symbol and model.
        """

        return (
            self.db.query(ModelMetrics)
            .filter(
                ModelMetrics.symbol == symbol,
                ModelMetrics.model_name == model_name
            )
            .order_by(
                ModelMetrics.created_at.desc()
            )
            .first()
        )

    # ---------------------------------------------------------
    # Exists
    # ---------------------------------------------------------

    def exists(
        self,
        symbol: str,
        model_name: str
    ) -> bool:

        return (
            self.find_by_model(
                symbol,
                model_name
            )
            is not None
        )

    # ---------------------------------------------------------
    # Delete One
    # ---------------------------------------------------------

    def delete(
        self,
        symbol: str,
        model_name: str
    ):

        metrics = self.find_by_model(
            symbol,
            model_name
        )

        if metrics is None:
            return False

        self.db.delete(metrics)
        self.db.commit()

        return True

    # ---------------------------------------------------------
    # Delete All
    # ---------------------------------------------------------

    def delete_all(
        self,
        symbol: str
    ):

        (
            self.db.query(ModelMetrics)
            .filter(
                ModelMetrics.symbol == symbol
            )
            .delete()
        )

        self.db.commit()