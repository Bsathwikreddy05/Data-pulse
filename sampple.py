import numpy as np
import pandas as pd

np.random.seed(42)
n_rows = 150

regions = ["North", "South", "East", "West"]
categories = ["Electronics", "Office Supplies", "Furniture", "Apparel"]
payment_methods = ["Credit Card", "UPI", "Debit Card", "Net Banking"]

# Generate base data
region_col = np.random.choice(regions, size=n_rows)
category_col = np.random.choice(categories, size=n_rows)
payment_col = np.random.choice(payment_methods, size=n_rows)

units_sold = np.random.randint(1, 20, size=n_rows)
unit_price = np.random.choice([15.0, 45.0, 120.0, 350.0, 850.0], size=n_rows)
total_revenue = units_sold * unit_price + np.random.normal(0, 10, size=n_rows)
total_revenue = np.round(np.maximum(total_revenue, 10.0), 2)

discount_pct = np.random.choice([0.0, 0.05, 0.10, 0.15, 0.25], size=n_rows)

# Dates across 2024
dates = pd.date_range(start="2024-01-01", periods=n_rows, freq="2D").strftime(
    "%Y-%m-%d"
)

df = pd.DataFrame(
    {
        "Order_Date": dates,
        "Region": region_col,
        "Category": category_col,
        "Payment_Method": payment_col,
        "Units_Sold": units_sold,
        "Unit_Price": unit_price,
        "Discount": discount_pct,
        "Total_Revenue": total_revenue,
    }
)

# 1. Inject Duplicates (5 duplicated rows)
duplicates = df.iloc[10:15].copy()
df = pd.concat([df, duplicates], ignore_index=True)

# 2. Inject Missing Values
df.loc[[5, 22, 60, 95], "Region"] = np.nan
df.loc[[12, 45, 88], "Units_Sold"] = np.nan
df.loc[[18, 70, 110], "Total_Revenue"] = np.nan

# 3. Inject Extreme Outliers (for IQR Outlier Table)
df.loc[3, "Total_Revenue"] = 45000.00  # Massive outlier
df.loc[50, "Total_Revenue"] = 38500.00  # Massive outlier
df.loc[80, "Units_Sold"] = 120  # Massive outlier

# Save CSV
df.to_csv("retail_test_data.csv", index=False)
print(" Successfully created 'retail_test_data.csv' with 155 rows!")