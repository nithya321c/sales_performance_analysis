from pathlib import Path
import sqlite3
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
CSV = ROOT / "data" / "sales_data_cleaned.csv"
DB = ROOT / "sales.db"

def main():
    df = pd.read_csv(CSV)
    df.columns = [
        "order_id","order_date","ship_date","customer_id","customer_name",
        "segment","country","city","state","region","product_id","category",
        "sub_category","product_name","sales","quantity","discount","profit"
    ]
    with sqlite3.connect(DB) as conn:
        df.to_sql("sales", conn, if_exists="replace", index=False)
        print(f"Loaded {len(df):,} rows into {DB}")
        queries = {
            "Overall KPIs": """SELECT ROUND(SUM(sales),2) total_sales,
                ROUND(SUM(profit),2) total_profit, COUNT(DISTINCT order_id) orders,
                SUM(quantity) units_sold FROM sales""",
            "Sales by category": """SELECT category, ROUND(SUM(sales),2) sales,
                ROUND(SUM(profit),2) profit FROM sales GROUP BY category ORDER BY sales DESC""",
            "Sales by region": """SELECT region, ROUND(SUM(sales),2) sales,
                ROUND(SUM(profit),2) profit FROM sales GROUP BY region ORDER BY profit DESC""",
            "Top products": """SELECT product_name, ROUND(SUM(sales),2) sales,
                ROUND(SUM(profit),2) profit FROM sales GROUP BY product_name ORDER BY sales DESC LIMIT 10"""
        }
        for title, query in queries.items():
            print(f"\\n=== {title} ===")
            print(pd.read_sql_query(query, conn).to_string(index=False))
    print("\\nDone. Database saved as sales.db")

if __name__ == "__main__":
    main()
