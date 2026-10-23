from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "data" / "sales_data_cleaned.csv"
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)

def main():
    df = pd.read_csv(INPUT, parse_dates=["Order Date", "Ship Date"])
    total_sales = df["Sales"].sum()
    total_profit = df["Profit"].sum()
    total_orders = df["Order ID"].nunique()
    total_units = df["Quantity"].sum()
    profit_margin = (total_profit / total_sales * 100) if total_sales else 0

    print("\\n=== OVERALL KPIs ===")
    print(f"Rows: {len(df):,}")
    print(f"Total sales: ${total_sales:,.2f}")
    print(f"Total profit: ${total_profit:,.2f}")
    print(f"Distinct orders: {total_orders:,}")
    print(f"Units sold: {total_units:,}")
    print(f"Profit margin: {profit_margin:.2f}%")

    summaries = {
        "sales_by_month.csv": df.assign(Month=df["Order Date"].dt.to_period("M").astype(str))
            .groupby("Month", as_index=False).agg(Sales=("Sales","sum"), Profit=("Profit","sum"), Orders=("Order ID","nunique")),
        "sales_by_category.csv": df.groupby("Category", as_index=False).agg(Sales=("Sales","sum"), Profit=("Profit","sum"), Quantity=("Quantity","sum")),
        "sales_by_region.csv": df.groupby("Region", as_index=False).agg(Sales=("Sales","sum"), Profit=("Profit","sum"), Orders=("Order ID","nunique")),
        "sales_by_subcategory.csv": df.groupby(["Category","Sub-Category"], as_index=False).agg(Sales=("Sales","sum"), Profit=("Profit","sum"), Quantity=("Quantity","sum")),
        "sales_by_segment.csv": df.groupby("Segment", as_index=False).agg(Sales=("Sales","sum"), Profit=("Profit","sum"), Orders=("Order ID","nunique")),
    }
    for filename, summary in summaries.items():
        summary.to_csv(OUT / filename, index=False)

    print(f"\\nSummary tables saved in: {OUT}")
    print("\\nTop 5 products by sales:")
    print(df.groupby("Product Name")["Sales"].sum().sort_values(ascending=False).head(5).round(2).to_string())
    print("\\nRegions with lowest profit:")
    print(df.groupby("Region")["Profit"].sum().sort_values().round(2).to_string())

if __name__ == "__main__":
    main()
