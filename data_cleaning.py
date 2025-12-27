import pandas as pd

# -----------------------------
# LOAD RAW DATA
# -----------------------------
df = pd.read_csv("D:\online_food_delivery\data\onlinedata.csv")

print("Original shape:", df.shape)

# -----------------------------
# REMOVE DUPLICATES
# -----------------------------
df.drop_duplicates(inplace=True)

# -----------------------------
# KEEP ONLY RELEVANT COLUMNS
# -----------------------------
required_columns = [
    "Order_ID",
    "Customer_ID",
    "Customer_Age",
    "Customer_Gender",
    "City",
    "Area",
    "Restaurant_Name",
    "Cuisine_Type",
    "Order_Status",
    "Order_Day",
    "Peak_Hour",
    "Payment_Mode",
    "Order_Value",
    "Final_Amount",
    "Profit_Margin",
    "Delivery_Rating",
    "Restaurant_Rating"
]

df = df[required_columns]

# -----------------------------
# DROP ROWS WITH MISSING CRITICAL DATA
# -----------------------------
df.dropna(inplace=True)

# -----------------------------
# REMOVE INVALID VALUES
# -----------------------------
df = df[df["Order_Value"] > 0]
df = df[df["Final_Amount"] > 0]

df = df[(df["Delivery_Rating"] >= 0) & (df["Delivery_Rating"] <= 5)]
df = df[(df["Restaurant_Rating"] >= 0) & (df["Restaurant_Rating"] <= 5)]

# -----------------------------
# FIX DATA TYPES
# -----------------------------
df["Customer_Age"] = df["Customer_Age"].astype(int)
df["Order_Value"] = df["Order_Value"].astype(float)
df["Final_Amount"] = df["Final_Amount"].astype(float)
df["Profit_Margin"] = df["Profit_Margin"].astype(float)

# -----------------------------
# FEATURE ENGINEERING
# -----------------------------

# Day type (use dataset definition)
df["Order_Day_Type"] = df["Order_Day"].apply(
    lambda x: "Weekend" if str(x).lower() in ["weekend", "sat", "sun"] else "Weekday"
)

# Peak hour flag (use given column)
df["Peak_Hour_Flag"] = df["Peak_Hour"].apply(
    lambda x: "Yes" if str(x).lower() in ["true", "1"] else "No"
)

# Profit margin %
# Profit Margin % (use dataset value directly)
df["Profit_Margin_Pct"] = df["Profit_Margin"].round(2)*100

# Customer age groups
df["Customer_Age_Group"] = pd.cut(
    df["Customer_Age"],
    bins=[0, 25, 35, 50, 100],
    labels=["18-25", "26-35", "36-50", "50+"]
)

# -----------------------------
# FINAL CLEANED DATASET
# -----------------------------
df.to_csv("D:\online_food_delivery\data\online_food_delivery_cleaned.csv", index=False)

print("Cleaning complete")
print("Final shape:", df.shape)
