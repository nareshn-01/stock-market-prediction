from sklearn.model_selection import GridSearchCV


class HyperparameterService:

    @staticmethod
    def tune(model, param_grid, X_train, y_train):

        search = GridSearchCV(
            estimator=model,
            param_grid=param_grid,
            cv=5,
            scoring="neg_root_mean_squared_error",
            n_jobs=-1
        )

        search.fit(X_train, y_train)

        return search.best_estimator_, search.best_params_