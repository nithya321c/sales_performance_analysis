-- Sales Performance Analysis (SQLite)
-- Run this script from the project root or use the command in README.md.
-- Dates are stored as ISO YYYY-MM-DD text, which sorts chronologically.

DROP TABLE IF EXISTS sales;
CREATE TABLE sales (
    order_id TEXT PRIMARY KEY,
    order_date TEXT,
    ship_date TEXT,
    customer_id TEXT,
    customer_name TEXT,
    segment TEXT,
    country TEXT,
    city TEXT,
    state TEXT,
    region TEXT,
    product_id TEXT,
    category TEXT,
    sub_category TEXT,
    product_name TEXT,
    sales REAL,
    quantity INTEGER,
    discount REAL,
    profit REAL
);

-- Import data using Python's sqlite3/pandas, or use the helper command in README.
-- The SELECT statements below can be run after the table is populated.

-- 1. Overall KPIs
SELECT
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit,
    COUNT(DISTINCT order_id) AS distinct_orders,
    SUM(quantity) AS units_sold,
    ROUND(100.0 * SUM(profit) / NULLIF(SUM(sales), 0), 2) AS profit_margin_pct
FROM sales;

-- 2. Sales and profit by category
SELECT category, ROUND(SUM(sales), 2) AS total_sales,
       ROUND(SUM(profit), 2) AS total_profit
FROM sales
GROUP BY category
ORDER BY total_sales DESC;

-- 3. Monthly performance
SELECT substr(order_date, 1, 7) AS month,
       ROUND(SUM(sales), 2) AS total_sales,
       ROUND(SUM(profit), 2) AS total_profit,
       COUNT(DISTINCT order_id) AS orders
FROM sales
GROUP BY substr(order_date, 1, 7)
ORDER BY month;

-- 4. Regional performance
SELECT region, ROUND(SUM(sales), 2) AS total_sales,
       ROUND(SUM(profit), 2) AS total_profit
FROM sales
GROUP BY region
ORDER BY total_profit DESC;

-- 5. Top 10 products by sales
SELECT product_name, ROUND(SUM(sales), 2) AS total_sales,
       ROUND(SUM(profit), 2) AS total_profit
FROM sales
GROUP BY product_name
ORDER BY total_sales DESC
LIMIT 10;

-- 6. Products with negative total profit (investigate, don't assume error)
SELECT product_name, category, sub_category,
       ROUND(SUM(sales), 2) AS total_sales,
       ROUND(SUM(profit), 2) AS total_profit
FROM sales
GROUP BY product_name, category, sub_category
HAVING SUM(profit) < 0
ORDER BY total_profit ASC;

-- 7. Performance by customer segment
SELECT segment, ROUND(SUM(sales), 2) AS total_sales,
       ROUND(SUM(profit), 2) AS total_profit,
       COUNT(DISTINCT order_id) AS orders
FROM sales
GROUP BY segment
ORDER BY total_sales DESC;
