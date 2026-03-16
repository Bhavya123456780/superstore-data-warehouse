import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

CSV_PATH = os.getenv("CSV_PATH", "superstore.csv")

def extract():
    print(f"Reading data from {CSV_PATH}...")
    df = pd.read_csv(CSV_PATH, encoding="latin-1")
    print(f"✓ Loaded {len(df)} rows and {len(df.columns)} columns")
    print(f"  Columns: {list(df.columns)}")
    return df

if __name__ == "__main__":
    df = extract()
    print(df.head())