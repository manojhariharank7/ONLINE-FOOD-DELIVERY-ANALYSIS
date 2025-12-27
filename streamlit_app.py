import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Food Delivery Dashboard", layout="wide")
st.title(" Online Food Delivery KPI Dashboard")

# ---------------- DB CONNECTION ----------------
engine = create_engine(
    "mysql+mysqlconnector://root:root@localhost/food_delivery"
)

@st.cache_data
def load_data():
    return pd.read_sql("SELECT * FROM orders", engine)

df = load_data()

# ---------------- SIDEBAR FILTERS ----------------
st.sidebar.header("Filters")

city_filter = st.sidebar.multiselect(
    "Select City",
    options=sorted(df["City"].unique()),
    default=sorted(df["City"].unique())
)

cuisine_filter = st.sidebar.multiselect(
    "Select Cuisine",
    options=sorted(df["Cuisine_Type"].unique()),
    default=sorted(df["Cuisine_Type"].unique())
)

status_filter = st.sidebar.multiselect(
    "Select Order Status",
    options=sorted(df["Order_Status"].unique()),
    default=sorted(df["Order_Status"].unique())
)

day_filter = st.sidebar.multiselect(
    "Select Day Type",
    options=sorted(df["Order_Day_Type"].unique()),
    default=sorted(df["Order_Day_Type"].unique())
)

# ---------------- APPLY FILTERS ----------------
filtered_df = df[
    (df["City"].isin(city_filter)) &
    (df["Cuisine_Type"].isin(cuisine_filter)) &
    (df["Order_Status"].isin(status_filter)) &
    (df["Order_Day_Type"].isin(day_filter))
]

# ---------------- KPIs ----------------
st.subheader("Key Performance Indicators")

c1, c2, c3, c4 = st.columns(4)

c1.metric("Total Orders", len(filtered_df))
c2.metric("Total Revenue", f"₹ {filtered_df['Order_Value'].sum():,.0f}")
c3.metric("Avg Order Value", f"₹ {filtered_df['Order_Value'].mean():.2f}")
c4.metric("Avg Profit Margin (%)", f"{filtered_df['Profit_Margin_Pct'].mean():.2f}")

st.divider()

# ---------------- PERFORMANCE METRICS ----------------
st.subheader(" Performance Metrics")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**Orders by City**")
    city_orders = filtered_df["City"].value_counts().reset_index()
    city_orders.columns = ["City", "Total Orders"]
    city_orders.index += 1
    st.dataframe(city_orders)

with col2:
    st.markdown("**Orders by Cuisine**")
    cuisine_orders = filtered_df["Cuisine_Type"].value_counts().reset_index()
    cuisine_orders.columns = ["Cuisine Type", "Total Orders"]
    cuisine_orders.index += 1
    st.dataframe(cuisine_orders)

st.divider()

# ---------------- TRENDS ----------------
st.subheader(" Trends")

col3, col4 = st.columns(2)

with col3:
    st.markdown("**Peak vs Non‑Peak Orders**")
    peak_orders = filtered_df["Peak_Hour_Flag"].value_counts().reset_index()
    peak_orders.columns = ["Peak Hour", "Total Orders"]
    peak_orders.index += 1
    st.dataframe(peak_orders)

with col4:
    st.markdown("**Order Status Distribution**")
    status_orders = filtered_df["Order_Status"].value_counts().reset_index()
    status_orders.columns = ["Order Status", "Total Orders"]
    status_orders.index += 1
    st.dataframe(status_orders)
