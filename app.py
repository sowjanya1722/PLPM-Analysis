import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv("cleaned_data.csv")

# Fix if CSV is read as single column
if len(df.columns) == 1:
    df = df[df.columns[0]].str.split(',', expand=True)
    df.columns = df.iloc[0]
    df = df[1:]

# Clean column names
df.columns = df.columns.str.strip()

st.title("PLPM Analysis Dashboard")

# Sidebar filter
st.sidebar.header("Filter")

# Check if Division column exists
if "Division" not in df.columns:
    st.error("Division column not found!")
    st.write("Available columns:", df.columns)
    st.stop()

division = st.sidebar.multiselect(
    "Select Division",
    df["Division"].dropna().unique(),
    default=df["Division"].dropna().unique()
)

# Filter data
filtered_df = df[df["Division"].isin(division)]

# KPIs
st.subheader("Key Metrics")
col1, col2, col3 = st.columns(3)

total_sales = pd.to_numeric(filtered_df['Sales'], errors='coerce').sum()
total_profit = pd.to_numeric(filtered_df['Gross Profit'], errors='coerce').sum()

col1.metric("Total Sales", int(total_sales))
col2.metric("Total Profit", int(total_profit))

if total_sales != 0:
    avg_margin = (total_profit / total_sales) * 100
else:
    avg_margin = 0

col3.metric("Avg Margin (%)", round(avg_margin, 2))

# Profit by Division
st.subheader("Profit by Division")
division_profit = filtered_df.groupby("Division")['Gross Profit'].apply(pd.to_numeric, errors='coerce').sum()

fig1, ax1 = plt.subplots()
division_profit.plot(kind='bar', ax=ax1)
st.pyplot(fig1)

# Top Products
st.subheader("Top Products by Profit")
top_products = (
    filtered_df.groupby("Product Name")['Gross Profit']
    .apply(pd.to_numeric, errors='coerce')
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

fig2, ax2 = plt.subplots()
top_products.plot(kind='bar', ax=ax2)
st.pyplot(fig2)

# Cost vs Profit
st.subheader("Cost vs Profit")

fig3, ax3 = plt.subplots()
ax3.scatter(
    pd.to_numeric(filtered_df['Cost'], errors='coerce'),
    pd.to_numeric(filtered_df['Gross Profit'], errors='coerce'),
    alpha=0.5
)
ax3.set_xlabel("Cost")
ax3.set_ylabel("Profit")

st.pyplot(fig3)
