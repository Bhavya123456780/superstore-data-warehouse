import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    return psycopg2.connect(
        host     = os.getenv("DB_HOST"),
        port     = os.getenv("DB_PORT"),
        dbname   = os.getenv("DB_NAME"),
        user     = os.getenv("DB_USER"),
        password = os.getenv("DB_PASSWORD")
    )

def load_dim_customer(cursor, df):
    for _, row in df.iterrows():
        cursor.execute("""
            INSERT INTO dim_customer
                (customer_id, customer_name, segment)
            VALUES (%s, %s, %s)
            ON CONFLICT (customer_id) DO NOTHING
        """, (row["customer_id"],
              row["customer_name"],
              row["segment"]))
    print(f"✓ Loaded {len(df)} customers")

def load_dim_product(cursor, df):
    for _, row in df.iterrows():
        cursor.execute("""
            INSERT INTO dim_product
                (product_id, product_name, category, sub_category)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (product_id) DO NOTHING
        """, (row["product_id"],
              row["product_name"],
              row["category"],
              row["sub_category"]))
    print(f"✓ Loaded {len(df)} products")

def load_dim_region(cursor, df):
    for _, row in df.iterrows():
        cursor.execute("""
            INSERT INTO dim_region
                (region_id, region, state, city)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT DO NOTHING
        """, (int(row["region_id"]),
              row["region"],
              row["state"],
              row["city"]))
    print(f"✓ Loaded {len(df)} regions")

def load_dim_date(cursor, df):
    for _, row in df.iterrows():
        cursor.execute("""
            INSERT INTO dim_date
                (date_id, full_date, day, month, year, quarter)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT DO NOTHING
        """, (int(row["date_id"]),
              row["full_date"],
              int(row["day"]),
              int(row["month"]),
              int(row["year"]),
              int(row["quarter"])))
    print(f"✓ Loaded {len(df)} dates")

def load_fact_orders(cursor, df):
    for _, row in df.iterrows():
        cursor.execute("""
            INSERT INTO fact_orders
                (order_id, customer_id, product_id,
                 region_id, date_id,
                 sales, quantity, discount, profit)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT DO NOTHING
        """, (row["order_id"],
              row["customer_id"],
              row["product_id"],
              int(row["region_id"]),
              int(row["date_id"]),
              float(row["sales"]),
              int(row["quantity"]),
              float(row["discount"]),
              float(row["profit"])))
    print(f"✓ Loaded {len(df)} orders")

def load(dim_customer, dim_product,
         dim_region, dim_date, fact_orders):
    conn   = get_connection()
    cursor = conn.cursor()
    try:
        load_dim_customer(cursor, dim_customer)
        load_dim_product(cursor, dim_product)
        load_dim_region(cursor, dim_region)
        load_dim_date(cursor, dim_date)
        load_fact_orders(cursor, fact_orders)
        conn.commit()
        print("✓ All data loaded successfully")
    except Exception as e:
        conn.rollback()
        print(f"✗ Error: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    print("Load module ready")