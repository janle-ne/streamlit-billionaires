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
    'age': 'Age',
    'state': 'State'  # Assuming there's a 'state' column for location (you may need to adjust this)
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

# Add state filter logic
option = st.selectbox(
    'Please select state:',
    ('California', 'Florida', 'Texas', 'New York', 'Illinois')
)
st.caption(f"You selected: {option}")

# Filter data based on the selected state
filtered_df = df[df['State'] == option]

# Plot bar chart for filtered state
fig = px.bar(
    filtered_df,
    x="NetWorth",
    y="Age Group",
    orientation="h",
    color="Age Group",
    hover_data=["Name", "NetWorth"],
    title=f"Top 50 Billionaires by Age Group in {option}",
)

# Layout: chart and table
col1, col2 = st.columns([3, 2])

with col1:
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Summary Table")
    table = filtered_df.groupby("Age Group")[["NetWorth"]].count().rename(columns={"NetWorth": "Count"})
    table["Total Net Worth ($B)"] = filtered_df.groupby("Age Group")["NetWorth"].sum().round(2)
    st.dataframe(table)
