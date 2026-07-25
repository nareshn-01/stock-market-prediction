CREATE TABLE stocks (
                        id BIGSERIAL PRIMARY KEY,
                        symbol VARCHAR(20) UNIQUE NOT NULL,
                        exchange VARCHAR(10) NOT NULL,
                        company_name VARCHAR(150) NOT NULL,
                        sector VARCHAR(100),
                        isin VARCHAR(20)
);

CREATE TABLE price_history (
                               id BIGSERIAL PRIMARY KEY,

                               stock_id BIGINT NOT NULL,

                               timestamp TIMESTAMP NOT NULL,

                               open NUMERIC(15,2) NOT NULL,

                               high NUMERIC(15,2) NOT NULL,

                               low NUMERIC(15,2) NOT NULL,

                               close NUMERIC(15,2) NOT NULL,

                               volume BIGINT NOT NULL,

                               interval VARCHAR(10) NOT NULL,

                               CONSTRAINT fk_stock
                                   FOREIGN KEY (stock_id)
                                       REFERENCES stocks(id)
                                       ON DELETE CASCADE
);

CREATE INDEX idx_price_stock_time
    ON price_history(stock_id, timestamp DESC);