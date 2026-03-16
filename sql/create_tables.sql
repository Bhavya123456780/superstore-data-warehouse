-- Superstore Data Warehouse Star Schema

CREATE TABLE IF NOT EXISTS dim_customer (
    customer_id     VARCHAR(20) PRIMARY KEY,
    customer_name   VARCHAR(100),
    segment         VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS dim_product (
    product_id      VARCHAR(20) PRIMARY KEY,
    product_name    VARCHAR(200),
    category        VARCHAR(50),
    sub_category    VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS dim_region (
    region_id       SERIAL PRIMARY KEY,
    region          VARCHAR(50),
    state           VARCHAR(50),
    city            VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS dim_date (
    date_id         SERIAL PRIMARY KEY,
    full_date       DATE,
    day             INTEGER,
    month           INTEGER,
    year            INTEGER,
    quarter         INTEGER
);

CREATE TABLE IF NOT EXISTS fact_orders (
    order_id        VARCHAR(20),
    customer_id     VARCHAR(20) REFERENCES dim_customer(customer_id),
    product_id      VARCHAR(20) REFERENCES dim_product(product_id),
    region_id       INTEGER     REFERENCES dim_region(region_id),
    date_id         INTEGER     REFERENCES dim_date(date_id),
    sales           NUMERIC(10,2),
    quantity        INTEGER,
    discount        NUMERIC(4,2),
    profit          NUMERIC(10,2),
    PRIMARY KEY (order_id, product_id)
);