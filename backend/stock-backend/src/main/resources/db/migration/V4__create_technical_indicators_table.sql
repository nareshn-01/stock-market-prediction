CREATE TABLE technical_indicators (
                                      id BIGSERIAL PRIMARY KEY,

                                      stock_id BIGINT NOT NULL,
                                      timestamp TIMESTAMP NOT NULL,
                                      interval VARCHAR(20) NOT NULL DEFAULT '1d',

                                      sma_20 NUMERIC(18,6),
                                      sma_50 NUMERIC(18,6),
                                      sma_200 NUMERIC(18,6),

                                      ema_12 NUMERIC(18,6),
                                      ema_26 NUMERIC(18,6),

                                      rsi_14 NUMERIC(18,6),

                                      macd NUMERIC(18,6),
                                      macd_signal NUMERIC(18,6),
                                      macd_histogram NUMERIC(18,6),

                                      bb_upper NUMERIC(18,6),
                                      bb_middle NUMERIC(18,6),
                                      bb_lower NUMERIC(18,6),

                                      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                      updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                                      CONSTRAINT fk_technical_stock
                                          FOREIGN KEY (stock_id)
                                              REFERENCES stocks(id)
                                              ON DELETE CASCADE,

                                      CONSTRAINT uk_technical_indicator
                                          UNIQUE (stock_id, timestamp, interval)
);

CREATE INDEX idx_technical_stock_timestamp
    ON technical_indicators(stock_id, timestamp);