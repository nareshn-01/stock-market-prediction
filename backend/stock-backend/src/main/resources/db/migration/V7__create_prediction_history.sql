CREATE TABLE prediction_history (
                                    id SERIAL PRIMARY KEY,
                                    symbol VARCHAR(20) NOT NULL,
                                    current_price DOUBLE PRECISION NOT NULL,
                                    predicted_price DOUBLE PRECISION NOT NULL,
                                    change_percent DOUBLE PRECISION NOT NULL,
                                    signal VARCHAR(20) NOT NULL,
                                    prediction_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_prediction_symbol
    ON prediction_history(symbol);

CREATE INDEX idx_prediction_time
    ON prediction_history(prediction_time);