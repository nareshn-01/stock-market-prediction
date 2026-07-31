from logger import logger

from models.model_type import ModelType

from services.stock_service import StockService
from services.indicator_service import IndicatorService
from services.training_service import TrainingService
from services.prediction_service import PredictionService


class MarketPipelineService:
    """
    Executes the complete daily ML pipeline.
    """

    def __init__(
        self,
        stock_service: StockService,
        indicator_service: IndicatorService,
        training_service: TrainingService,
        prediction_service: PredictionService,
        stock_repository
    ):
        self.stock_service = stock_service
        self.indicator_service = indicator_service
        self.training_service = training_service
        self.prediction_service = prediction_service
        self.stock_repository = stock_repository

    # ---------------------------------------------------------
    # Complete Pipeline
    # ---------------------------------------------------------

    def run(
        self,
        model_type: ModelType = ModelType.LIGHTGBM,
        tune: bool = False
    ):

        logger.info("Starting Market Pipeline...")

        summary = {
            "updated": [],
            "trained": [],
            "predicted": [],
            "errors": []
        }

        stocks = self.stock_repository.get_all()

        for stock in stocks:

            logger.info(f"Processing {stock.symbol}")

            try:

                # -------------------------------------
                # Update price history
                # -------------------------------------

                update_result = self.stock_service.update_stock(
                    stock
                )

                summary["updated"].append(update_result)

                # -------------------------------------
                # Technical Indicators
                # -------------------------------------

                self.indicator_service.calculate(stock)

                # -------------------------------------
                # Train model
                # -------------------------------------

                train_result = self.training_service.train(
                    stock=stock,
                    model_type=model_type,
                    tune=tune
                )

                summary["trained"].append(train_result)

                # -------------------------------------
                # Predict
                # -------------------------------------

                prediction = self.prediction_service.predict(
                    stock=stock,
                    model_name=model_type.value
                )

                summary["predicted"].append(prediction)

            except Exception as ex:

                logger.exception(ex)

                summary["errors"].append({
                    "symbol": stock.symbol,
                    "error": str(ex)
                })

        logger.info("Market Pipeline Completed.")

        return summary

    # ---------------------------------------------------------
    # Update Only
    # ---------------------------------------------------------

    def update_market(self):

        logger.info("Updating market data...")

        return self.stock_service.refresh_all_stocks()

    # ---------------------------------------------------------
    # Train Only
    # ---------------------------------------------------------

    def train_market(
        self,
        model_type: ModelType = ModelType.LIGHTGBM,
        tune: bool = False
    ):

        results = []

        stocks = self.stock_repository.get_all()

        for stock in stocks:

            results.append(

                self.training_service.train(
                    stock=stock,
                    model_type=model_type,
                    tune=tune
                )

            )

        return results

    # ---------------------------------------------------------
    # Predict Only
    # ---------------------------------------------------------

    def predict_market(
        self,
        model_type: ModelType = ModelType.LIGHTGBM
    ):

        results = []

        stocks = self.stock_repository.get_all()

        for stock in stocks:

            prediction = self.prediction_service.predict(
                stock,
                model_type.value
            )

            results.append(prediction)

        return results