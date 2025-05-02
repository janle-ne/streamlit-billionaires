import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Gender Ratio of Billionaires", layout="wide")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("BillionairesData.csv")
    df = df.dropna(subset=["country", "gender"])  # Handle missing data
    return df

df = load_data()

st.title("🌍 Gender Ratio Comparison of Billionaires by Country")

# Select country
countries = df['country'].value_counts().index.tolist()
selected_country = st.selectbox("Select a country:", countries)

# Filter data by selected country
df_country = df[df['country'] == selected_country]

# Calculate gender ratio
gender_counts = df_country['gender'].value_counts().reset_index()
gender_counts.columns = ['Gender', 'Count']
gender_counts['Percentage'] = (gender_counts['Count'] / gender_counts['Count'].sum() * 100).round(2)

# Donut chart (Plotly)
fig = px.pie(
    gender_counts,
    values='Count',
    names='Gender',
    hole=0.5,
    color_discrete_sequence=px.colors.qualitative.Set3,
    title=f"Gender Distribution of Billionaires in {selected_country}"
)
fig.update_traces(textinfo='percent+label', hoverinfo='label+percent+value', pull=[0.05] * len(gender_counts))
fig.update_layout(
    showlegend=True,
    margin=dict(t=50, b=20),
    height=500
)

# Display chart and table
st.plotly_chart(fig, use_container_width=True)

st.subheader(f"Gender Statistics Table in {selected_country}")
st.dataframe(gender_counts)


