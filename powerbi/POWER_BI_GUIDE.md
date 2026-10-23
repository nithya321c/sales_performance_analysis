# Power BI Desktop Build Guide

## 1. Import data
1. Open Power BI Desktop.
2. Select **Get data → Text/CSV**.
3. Choose `data/sales_data_cleaned.csv`.
4. Select **Transform Data** to open Power Query.

## 2. Check data types in Power Query
- `Order Date`, `Ship Date`: Date
- `Sales`, `Profit`, `Discount`: Decimal number
- `Quantity`: Whole number
- IDs and descriptive columns: Text

Check column quality and look for unexpected nulls. Do not remove negative-profit transactions just because they are negative; negative profit can be a valid business outcome.

Choose **Close & Apply**.

## 3. Create a date table (recommended)
In Power BI, select **Modeling → New table** and paste:

```DAX
Calendar =
ADDCOLUMNS (
    CALENDAR ( MIN ( Sales[Order Date] ), MAX ( Sales[Order Date] ) ),
    "Year", YEAR ( [Date] ),
    "Month Number", MONTH ( [Date] ),
    "Month", FORMAT ( [Date], "MMM" ),
    "Year-Month", FORMAT ( [Date], "YYYY-MM" )
)
```

Replace `Sales` with the actual table name if Power BI uses a different name. Create a relationship from `Calendar[Date]` to `Sales[Order Date]`. Sort `Calendar[Month]` by `Calendar[Month Number]`. For a multi-year trend, use `Year-Month` on the axis so months from different years don't combine.

## 4. Create measures
Select **Modeling → New measure** for each:

```DAX
Total Sales = SUM ( Sales[Sales] )

Total Profit = SUM ( Sales[Profit] )

Total Orders = DISTINCTCOUNT ( Sales[Order ID] )

Units Sold = SUM ( Sales[Quantity] )

Profit Margin % = DIVIDE ( [Total Profit], [Total Sales], 0 )
```

Format `Total Sales` and `Total Profit` as currency; format `Profit Margin %` as percentage. If using the synthetic dataset, the measures should aggregate all rows and respond to slicers.

## 5. Build the report page
Suggested layout:
- Top row: Card visuals for Total Sales, Total Profit, Total Orders, Units Sold, Profit Margin %.
- Middle left: Line chart with `Calendar[Year-Month]` on X-axis and `[Total Sales]` on Y-axis.
- Middle right: Clustered column chart with `Sales[Category]` on X-axis and `[Total Sales]` on Y-axis.
- Bottom left: Bar chart with `Sales[Region]` and `[Total Profit]`.
- Bottom right: Bar chart with `Sales[Product Name]` and `[Total Sales]`; apply Top N = 10 by `[Total Sales]`.
- Slicers: `Calendar[Year]`, `Sales[Region]`, `Sales[Category]`, `Sales[Segment]`.

## 6. Validate the dashboard
- With no filters selected, compare card totals to the Python script output.
- The sales and profit totals should match the sums from `python/analyze_data.py`.
- Change one slicer and verify that the KPI cards and charts update.
- Ensure the monthly axis is chronological, not alphabetic.
- Save as `Sales_Performance_Analysis.pbix` in the project root.

## 7. Suggested design
Use a consistent 2–3 colour palette, aligned visuals, descriptive titles, readable labels and enough whitespace. Avoid 3D charts. Add a small subtitle: “Synthetic practice dataset | 2023–2025”.
