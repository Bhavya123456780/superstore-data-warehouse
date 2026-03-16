import pandas as pd
from datetime import datetime

def transform(df):
    print("Starting transformation...")

    # clean column names — remove spaces
    df.columns = df.columns.str.strip().str.replace(" ", "_").str.lower()
    print(f"✓ Cleaned column names")

    # drop nulls in critical columns
    df = df.dropna(subset=["order_id", "customer_id", "product_id"])
    df = df.drop_duplicates()
    print(f"✓ Removed nulls and duplicates — {len(df)} rows remaining")

    # fix date columns
    df["order_date"]  = pd.to_datetime(df["order_date"])
    df["ship_date"]   = pd.to_datetime(df["ship_date"])
    print(f"✓ Parsed date columns")

    # fix numeric columns
    df["sales"]    = df["sales"].astype(float)
    df["quantity"] = df["quantity"].astype(int)
    df["discount"] = df["discount"].astype(float)
    df["profit"]   = df["profit"].astype(float)
    print(f"✓ Fixed numeric types")

    # ── dim_customer ──
    dim_customer = df[["customer_id", "customer_name", "segment"]] \
        .drop_duplicates(subset=["customer_id"]) \
        .reset_index(drop=True)

    # ── dim_product ──
    dim_product = df[["product_id", "product_name", "category", "sub-category"]] \
        .rename(columns={"sub-category": "sub_category"}) \
        .drop_duplicates(subset=["product_id"]) \
        .reset_index(drop=True)

    # ── dim_region ──
    dim_region = df[["region", "state", "city"]] \
        .drop_duplicates() \
        .reset_index(drop=True)
    dim_region["region_id"] = dim_region.index + 1

    # ── dim_date ──
    dim_date = df[["order_date"]].drop_duplicates().copy()
    dim_date["date_id"] = dim_date.index + 1
    dim_date["full_date"] = dim_date["order_date"].dt.date
    dim_date["day"]       = dim_date["order_date"].dt.day
    dim_date["month"]     = dim_date["order_date"].dt.month
    dim_date["year"]      = dim_date["order_date"].dt.year
    dim_date["quarter"]   = dim_date["order_date"].dt.quarter
    dim_date = dim_date.drop(columns=["order_date"])

    # ── fact_orders ──
    fact = df.merge(
        dim_region, on=["region", "state", "city"]
    ).merge(
        dim_date.assign(order_date=pd.to_datetime(
            dim_date["full_date"]
        )),
        left_on="order_date", right_on="order_date",
        how="left"
    )
    fact_orders = fact[[
        "order_id", "customer_id", "product_id",
        "region_id", "date_id",
        "sales", "quantity", "discount", "profit"
    ]].drop_duplicates(subset=["order_id", "product_id"])

    print(f"✓ dim_customer: {len(dim_customer)} rows")
    print(f"✓ dim_product:  {len(dim_product)} rows")
    print(f"✓ dim_region:   {len(dim_region)} rows")
    print(f"✓ dim_date:     {len(dim_date)} rows")
    print(f"✓ fact_orders:  {len(fact_orders)} rows")

    return dim_customer, dim_product, dim_region, dim_date, fact_orders

if __name__ == "__main__":
    from extract import extract
    df = extract()
    transform(df)