from pathlib import Path
import pandas as pd
import streamlit as st
import plotly.express as px

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data" / "sales_data_cleaned.csv"

st.set_page_config(page_title="Sales Performance Analysis", page_icon="📊", layout="wide")
st.title("📊 Sales Performance Analysis")
st.caption("Portfolio project • Synthetic practice dataset • 2023–2025")

@st.cache_data
def load_data():
    df = pd.read_csv(DATA, parse_dates=["Order Date", "Ship Date"])
    return df

df = load_data()
with st.sidebar:
    st.header("Filters")
    date_min, date_max = df["Order Date"].min().date(), df["Order Date"].max().date()
    dates = st.date_input("Order date range", value=(date_min, date_max), min_value=date_min, max_value=date_max)
    regions = st.multiselect("Region", sorted(df["Region"].dropna().unique()), default=sorted(df["Region"].dropna().unique()))
    categories = st.multiselect("Category", sorted(df["Category"].dropna().unique()), default=sorted(df["Category"].dropna().unique()))
    segments = st.multiselect("Customer segment", sorted(df["Segment"].dropna().unique()), default=sorted(df["Segment"].dropna().unique()))

filtered = df.copy()
if isinstance(dates, (tuple, list)) and len(dates) == 2:
    filtered = filtered[(filtered["Order Date"].dt.date >= dates[0]) & (filtered["Order Date"].dt.date <= dates[1])]
filtered = filtered[filtered["Region"].isin(regions) & filtered["Category"].isin(categories) & filtered["Segment"].isin(segments)]

sales = filtered["Sales"].sum()
profit = filtered["Profit"].sum()
orders = filtered["Order ID"].nunique()
units = filtered["Quantity"].sum()
margin = (profit / sales * 100) if sales else 0

c1,c2,c3,c4,c5 = st.columns(5)
c1.metric("Total Sales", f"${sales:,.0f}")
c2.metric("Total Profit", f"${profit:,.0f}")
c3.metric("Distinct Orders", f"{orders:,}")
c4.metric("Units Sold", f"{units:,}")
c5.metric("Profit Margin", f"{margin:.1f}%")

monthly = filtered.assign(Month=filtered["Order Date"].dt.to_period("M").dt.to_timestamp()).groupby("Month", as_index=False).agg(Sales=("Sales","sum"), Profit=("Profit","sum"))
left, right = st.columns(2)
with left:
    st.subheader("Monthly sales trend")
    fig = px.line(monthly, x="Month", y="Sales", markers=True, title="Sales by month")
    st.plotly_chart(fig, use_container_width=True)
with right:
    st.subheader("Sales by category")
    by_cat = filtered.groupby("Category", as_index=False).agg(Sales=("Sales","sum"), Profit=("Profit","sum")).sort_values("Sales", ascending=False)
    fig = px.bar(by_cat, x="Category", y="Sales", color="Category", title="Revenue by category")
    st.plotly_chart(fig, use_container_width=True)

left, right = st.columns(2)
with left:
    st.subheader("Regional performance")
    by_region = filtered.groupby("Region", as_index=False).agg(Sales=("Sales","sum"), Profit=("Profit","sum")).sort_values("Sales", ascending=False)
    fig = px.bar(by_region, x="Region", y=["Sales","Profit"], barmode="group", title="Sales and profit by region")
    st.plotly_chart(fig, use_container_width=True)
with right:
    st.subheader("Top 10 products by sales")
    top_products = filtered.groupby("Product Name", as_index=False).agg(Sales=("Sales","sum"), Profit=("Profit","sum")).nlargest(10, "Sales")
    fig = px.bar(top_products.sort_values("Sales"), x="Sales", y="Product Name", orientation="h", title="Top products")
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Filtered data preview")
st.dataframe(filtered.head(100), use_container_width=True)
st.download_button("Download filtered data as CSV", filtered.to_csv(index=False).encode("utf-8"), "filtered_sales_data.csv", "text/csv")

st.info("This dashboard uses synthetic data generated for learning. Do not interpret the results as real company performance.")
