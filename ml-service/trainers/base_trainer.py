from abc import ABC, abstractmethod


class BaseTrainer(ABC):

    @abstractmethod
    def train(
        self,
        X_train,
        y_train,
        tune: bool = False
    ):
        """
        Train the model.

        Parameters
        ----------
        X_train : Training features
        y_train : Training labels
        tune : False -> Fast training
               True  -> Hyperparameter tuning
        """
        pass

    @abstractmethod
    def predict(
        self,
        X_test
    ):
        """
        Predict values for the given features.
        """
        pass

    @abstractmethod
    def save(
        self,
        symbol: str
    ):
        """
        Save the trained model.
        """
        pass

    @property
    @abstractmethod
    def model_name(self):
        """
        Name of the ML algorithm.
        """
        pass

    @property
    @abstractmethod
    def version(self):
        """
        Model version.
        """
        pass

    @property
    @abstractmethod
    def estimator(self):
        """
        Return the underlying estimator.
        """
        pass

    @property
    @abstractmethod
    def parameters(self):
        """
        Return the parameters used for training.
        """
        pass