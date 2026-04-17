import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv("cleaned_data.csv")

# Clean column names
df.columns = df.columns.str.strip()

st.title("PLPM Analysis Dashboard")

# Sidebar filter
st.sidebar.header("Filter")

division = st.sidebar.multiselect(
    "Select Division",
    df["Division"].unique(),
    default=df["Division"].unique()
)

filtered_df = df[df["Division"].isin(division)]

# KPIs
st.subheader("Key Metrics")
col1, col2, col3 = st.columns(3)

col1.metric("Total Sales", int(filtered_df['Sales'].sum()))
col2.metric("Total Profit", int(filtered_df['Gross Profit'].sum()))
col3.metric("Avg Margin (%)", round((filtered_df['Gross Profit'].sum() / filtered_df['Sales'].sum()) * 100, 2))

# Profit by Division
st.subheader("Profit by Division")
division_profit = filtered_df.groupby("Division")['Gross Profit'].sum()

fig1, ax1 = plt.subplots()
division_profit.plot(kind='bar', ax=ax1)
st.pyplot(fig1)

# Top Products
st.subheader("Top Products by Profit")
top_products = filtered_df.groupby("Product Name")['Gross Profit'].sum().sort_values(ascending=False).head(10)

fig2, ax2 = plt.subplots()
top_products.plot(kind='bar', ax=ax2)
st.pyplot(fig2)

# Cost vs Profit
st.subheader("Cost vs Profit")
fig3, ax3 = plt.subplots()
ax3.scatter(filtered_df['Cost'], filtered_df['Gross Profit'], alpha=0.5)
ax3.set_xlabel("Cost")
ax3.set_ylabel("Profit")
st.pyplot(fig3)
