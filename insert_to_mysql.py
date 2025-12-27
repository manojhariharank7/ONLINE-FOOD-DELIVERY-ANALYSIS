import pandas as pd
from sqlalchemy import create_engine

# Load cleaned CSV
df = pd.read_csv("D:\online_food_delivery\data\online_food_delivery_cleaned.csv")

# MySQL connection (edit password if needed)
engine = create_engine(
    "mysql+mysqlconnector://root:root@localhost/food_delivery"
)

# Insert into MySQL
df.to_sql(
    name="orders",
    con=engine,
    if_exists="append",
    index=False
)

print("Cleaned data inserted into MySQL successfully")
