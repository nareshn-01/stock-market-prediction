from sqlalchemy import desc
from sqlalchemy.orm import Session

from models.prediction_history import PredictionHistory


class PredictionRepository:

    def __init__(
        self,
        db: Session
    ):
        self.db = db

    def save(
        self,
        prediction: PredictionHistory
    ) -> PredictionHistory:
        """
        Save prediction history.
        """

        self.db.add(prediction)
        self.db.commit()
        self.db.refresh(prediction)

        return prediction

    def get_history(
        self,
        symbol: str,
        limit: int = 100
    ):
        """
        Return prediction history ordered by newest first.
        """

        return (
            self.db.query(PredictionHistory)
            .filter(
                PredictionHistory.symbol == symbol.upper()
            )
            .order_by(
                desc(PredictionHistory.created_at)
            )
            .limit(limit)
            .all()
        )

    def get_latest(
        self,
        symbol: str
    ):
        """
        Return latest prediction.
        """

        return (
            self.db.query(PredictionHistory)
            .filter(
                PredictionHistory.symbol == symbol.upper()
            )
            .order_by(
                desc(PredictionHistory.created_at)
            )
            .first()
        )

    def get_by_signal(
        self,
        symbol: str,
        signal: str,
        limit: int = 100
    ):
        """
        Return predictions filtered by signal.
        """

        return (
            self.db.query(PredictionHistory)
            .filter(
                PredictionHistory.symbol == symbol.upper(),
                PredictionHistory.signal == signal.upper()
            )
            .order_by(
                desc(PredictionHistory.created_at)
            )
            .limit(limit)
            .all()
        )

    def count(
        self,
        symbol: str
    ) -> int:
        """
        Count stored predictions.
        """

        return (
            self.db.query(PredictionHistory)
            .filter(
                PredictionHistory.symbol == symbol.upper()
            )
            .count()
        )

    def exists(
        self,
        symbol: str
    ) -> bool:
        """
        Check whether prediction history exists.
        """

        return self.count(symbol) > 0

    def delete_history(
        self,
        symbol: str
    ) -> int:
        """
        Delete all prediction history for a stock.

        Returns:
            Number of deleted records.
        """

        deleted = (
            self.db.query(PredictionHistory)
            .filter(
                PredictionHistory.symbol == symbol.upper()
            )
            .delete(
                synchronize_session=False
            )
        )

        self.db.commit()

        return deleted