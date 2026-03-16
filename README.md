# superstore-data-warehouse
Retail sales data warehouse with Star Schema, Python ETL, SQL analytics and dbt transformations# Superstore Sales Data Warehouse 

A data warehousing project that transforms raw retail sales data into
an analytics-ready Star Schema using Python ETL, PostgreSQL, SQL
analytics, and dbt transformation models.

## Architecture
```
superstore.csv (10K rows)
       |
   extract.py          ← load raw CSV
       |
  transform.py         ← clean + split into 5 tables
       |
    load.py            ← insert into PostgreSQL
       |
  PostgreSQL           ← Star Schema data warehouse
       |
  analytics.sql        ← business insights queries
       |
  dbt models           ← transformation layer
```

## Data Model — Star Schema
```
dim_customer       dim_product
     \                /
      \              /
       fact_orders
      /              \
     /                \
dim_region          dim_date
```

## Tech Stack

- **Python** — ETL pipeline logic
- **Pandas** — data cleaning and transformation
- **PostgreSQL** — data warehouse
- **dbt** — transformation layer and data quality tests
- **Docker** — containerized database
- **SQL** — analytics queries with window functions

## Project Structure
```
superstore-data-warehouse/
├── src/
│   ├── extract.py          # Load CSV into DataFrame
│   ├── transform.py        # Split into Star Schema tables
│   └── load.py             # Insert into PostgreSQL
├── sql/
│   ├── create_tables.sql   # Star Schema DDL
│   └── analytics.sql       # 6 analytical SQL queries
├── dbt_project/            # dbt transformation models
├── requirements.txt
└── .env                    # credentials (not committed)
```

## Key SQL Analytics

- Revenue and profit by category
- Monthly revenue trend over time
- Top 10 customers by lifetime value
- Regional sales performance
- Product ranking with RANK() window function
- Quarter over quarter growth with LAG() window function

## Setup & Run

### 1. Clone the repo
```bash
git clone https://github.com/Bhavya123456780/superstore-data-warehouse.git
cd superstore-data-warehouse
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Add credentials to .env
```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=superstoredb
DB_USER=postgres
DB_PASSWORD=postgres
CSV_PATH=superstore.csv
```

### 4. Start PostgreSQL
```bash
docker-compose up -d
```

### 5. Create tables
```bash
psql -h localhost -U postgres -d superstoredb -f sql/create_tables.sql
```

### 6. Run the pipeline
```bash
python src/extract.py
python src/transform.py
python src/load.py
```

### 7. Run analytics queries
```bash
psql -h localhost -U postgres -d superstoredb -f sql/analytics.sql
```

## Author
Bhavya Sri Muddana — [github.com/Bhavya123456780](https://github.com/Bhavya123456780)
