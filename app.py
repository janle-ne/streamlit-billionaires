import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")
st.title("Top 50 Billionaires by Net Worth (2023)")

# Load dataset
df = pd.read_csv("BillionairesData.csv", encoding="utf-8-sig")

# Rename columns for clarity
df.rename(columns={
    'finalWorth': 'NetWorth',
    'personName': 'Name',
    'age': 'Age'
}, inplace=True)

# Drop missing Age or NetWorth
df = df.dropna(subset=["Age", "NetWorth"])

# Sort top 50 richest
df = df.sort_values(by='NetWorth', ascending=False).head(50)

# Age group function
def get_age_group(age):
    if age < 30:
        return "Under 30"
    elif age <= 50:
        return "31-50"
    elif age <= 70:
        return "51-70"
    else:
        return "Over 70"

# Apply age group
df["Age Group"] = df["Age"].apply(get_age_group)

# Plot bar chart
fig = px.bar(
    df,
    x="NetWorth",
    y="Age Group",
    orientation="h",
    color="Age Group",
    hover_data=["Name", "NetWorth"],
    title="Top 50 Billionaires by Age Group",
)

# Layout: chart and table
col1, col2 = st.columns([3, 2])

with col1:
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Summary Table")
    table = df.groupby("Age Group")[["NetWorth"]].count().rename(columns={"NetWorth": "Count"})
    table["Total Net Worth ($B)"] = df.groupby("Age Group")["NetWorth"].sum().round(2)
    st.dataframe(table)
