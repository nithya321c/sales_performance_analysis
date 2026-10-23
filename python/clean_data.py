from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "data" / "sales_data_raw.csv"
OUTPUT = ROOT / "data" / "sales_data_cleaned.csv"

def main():
    df = pd.read_csv(INPUT)
    print(f"Rows loaded: {len(df):,}")
    print(f"Duplicate rows before cleaning: {df.duplicated().sum():,}")

    # Normalize text fields
    text_cols = ["Segment", "Country", "City", "State", "Region",
                 "Category", "Sub-Category", "Product Name"]
    for col in text_cols:
        df[col] = df[col].astype("string").str.strip()

    # Convert dates and numeric columns; invalid values become missing and are reported
    for col in ["Order Date", "Ship Date"]:
        df[col] = pd.to_datetime(df[col], errors="coerce")
    for col in ["Sales", "Quantity", "Discount", "Profit"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    missing = df.isna().sum()
    print("Missing values by column:")
    print(missing[missing > 0].to_string() if (missing > 0).any() else "None")

    # Remove exact duplicate rows only. Do not remove loss-making orders automatically.
    before = len(df)
    df = df.drop_duplicates()
    print(f"Exact duplicate rows removed: {before - len(df):,}")

    # Keep the original business values; export dates in a consistent format.
    df.to_csv(OUTPUT, index=False, date_format="%Y-%m-%d")
    print(f"Saved cleaned data to: {OUTPUT}")
    print(f"Rows after cleaning: {len(df):,}")
    print(f"Total sales: {df['Sales'].sum():,.2f}")
    print(f"Total profit: {df['Profit'].sum():,.2f}")

if __name__ == "__main__":
    main()
