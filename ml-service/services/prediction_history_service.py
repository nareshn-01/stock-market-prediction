from repositories.prediction_repository import (
    PredictionRepository
)


class PredictionHistoryService:

    def __init__(
        self,
        prediction_repository: PredictionRepository
    ):
        self.prediction_repository = prediction_repository

    def get_history(
        self,
        symbol: str,
        limit: int = 100
    ):
        """
        Return prediction history for a stock.
        """

        return self.prediction_repository.get_history(
            symbol=symbol.upper(),
            limit=limit
        )

    def get_latest(
        self,
        symbol: str
    ):
        """
        Return the latest prediction.
        """

        return self.prediction_repository.get_latest(
            symbol.upper()
        )

    def delete_history(
        self,
        symbol: str
    ):
        """
        Delete prediction history.
        """

        deleted = self.prediction_repository.delete_history(
            symbol.upper()
        )

        return {
            "symbol": symbol.upper(),
            "deleted_records": deleted
        }

    def count(
        self,
        symbol: str
    ) -> int:
        """
        Return number of stored predictions.
        """

        history = self.prediction_repository.get_history(
            symbol.upper(),
            limit=100000
        )

        return len(history)

    def exists(
        self,
        symbol: str
    ) -> bool:
        """
        Check whether prediction history exists.
        """

        latest = self.prediction_repository.get_latest(
            symbol.upper()
        )

        return latest is not None