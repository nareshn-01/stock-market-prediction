from abc import ABC, abstractmethod


class BaseTrainer(ABC):

    @abstractmethod
    def train(
        self,
        X_train,
        y_train
    ):
        """
        Train the model.
        """
        pass

    @abstractmethod
    def predict(
        self,
        X_test
    ):
        """
        Predict values.
        """
        pass

    @abstractmethod
    def save(
        self,
        symbol: str
    ):
        """
        Save trained model.
        """
        pass

    @property
    @abstractmethod
    def model_name(self):
        """
        Return model name.
        """
        pass

    @property
    @abstractmethod
    def version(self):
        """
        Return model version.
        """
        pass