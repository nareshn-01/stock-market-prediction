from sklearn.model_selection import RandomizedSearchCV


class HyperparameterService:

    @staticmethod
    def tune(
        model,
        param_grid,
        X_train,
        y_train,
        n_iter=10,
        cv=3
    ):
        """
        Tune hyperparameters using RandomizedSearchCV.

        Faster than GridSearchCV because it evaluates only a
        subset of parameter combinations.
        """

        search = RandomizedSearchCV(
            estimator=model,
            param_distributions=param_grid,
            n_iter=n_iter,
            cv=cv,
            scoring="neg_root_mean_squared_error",
            random_state=42,
            n_jobs=-1
        )

        search.fit(
            X_train,
            y_train
        )

        return (
            search.best_estimator_,
            search.best_params_
        )