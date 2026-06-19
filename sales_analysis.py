import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('sales_data.csv')

print("=" * 60)
print("SALES DATA ANALYSIS".center(60))
print("=" * 60)

print("\n[1] Dataset Shape:")
print(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")

print("\n[2] Column Names:")
print(df.columns.tolist())

print("\n[3] Missing Values:")
print(df.isnull().sum())

print("\n[4] Duplicate Check:")
print(f"Duplicate Orders: {df['OrderID'].duplicated().sum()}")

print("\n[5] Payment Methods:")
print(df['PaymentMethod'].value_counts())

print("\n[6] Order Status:")
print(df['OrderStatus'].value_counts())

print("\n[7] Top 5 Products by Revenue:")
top_products = df.groupby('Product')['TotalPrice'].sum().sort_values(ascending=False)
print(top_products.head())

print("\n[8] Revenue by Channel:")
channel_revenue = df.groupby('ReferralSource')['TotalPrice'].sum().sort_values(ascending=False)
print(channel_revenue)

print("\n[9] Monthly Sales Trend:")
df['Date'] = pd.to_datetime(df['Date'])
df['Month'] = df['Date'].dt.to_period('M')
monthly_sales = df.groupby('Month')['TotalPrice'].sum()
print(monthly_sales)

print("\n" + "=" * 60)
print("ANALYSIS COMPLETE".center(60))
print("=" * 60)