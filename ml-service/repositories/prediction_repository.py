from sqlalchemy.orm import Session

from models.prediction_history import PredictionHistory


class PredictionRepository:

    def __init__(self, db: Session):
        self.db = db

    def save(
        self,
        prediction: PredictionHistory
    ) -> PredictionHistory:

        self.db.add(prediction)
        self.db.commit()
        self.db.refresh(prediction)

        return prediction

    def get_latest(
        self,
        symbol: str
    ):

        return (
            self.db.query(PredictionHistory)
            .filter(
                PredictionHistory.symbol == symbol.upper()
            )
            .order_by(
                PredictionHistory.prediction_time.desc()
            )
            .first()
        )

    def get_history(
        self,
        symbol: str,
        limit: int = 100
    ):

        return (
            self.db.query(PredictionHistory)
            .filter(
                PredictionHistory.symbol == symbol.upper()
            )
            .order_by(
                PredictionHistory.prediction_time.desc()
            )
            .limit(limit)
            .all()
        )

    def delete_history(
        self,
        symbol: str
    ) -> int:

        deleted = (
            self.db.query(PredictionHistory)
            .filter(
                PredictionHistory.symbol == symbol.upper()
            )
            .delete()
        )

        self.db.commit()

        return deleted

    def get_all(
        self,
        limit: int = 100
    ):

        return (
            self.db.query(PredictionHistory)
            .order_by(
                PredictionHistory.prediction_time.desc()
            )
            .limit(limit)
            .all()
        )

    def count(
        self,
        symbol: str
    ) -> int:

        return (
            self.db.query(PredictionHistory)
            .filter(
                PredictionHistory.symbol == symbol.upper()
            )
            .count()
        )