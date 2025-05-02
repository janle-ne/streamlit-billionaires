import streamlit as st
import pandas as pd
import plotly.express as px

# Giao diện rộng
st.set_page_config(page_title="Gender Ratio of Billionaires", layout="wide")

# CSS highlight pastel
st.markdown("""
<style>
.highlight {
    background-color: #e6f7ff;
    padding: 4px 8px;
    border-radius: 8px;
    font-weight: 500;
}
</style>
""", unsafe_allow_html=True)

# Nội dung giới thiệu có highlight
st.title("🌍 Gender Ratio Comparison of Billionaires by Country")
st.markdown("""
### **Exploring Gender Inequality Among the World's Richest**

Despite global movements toward equality, the world of extreme wealth remains **disproportionately male-dominated**. This section explores the **gender ratio** of billionaires across different countries.

Some countries show a strong **imbalance**, while others have made strides toward more inclusive economic growth. By analyzing this data, we can better understand how **gender representation** in extreme wealth varies globally.

### **Key Observations:**
- In many nations, <span class="highlight">Male billionaires</span> significantly outnumber <span class="highlight">Female billionaires</span>.
- Societal, economic, and historical factors influence this imbalance.
- Which countries are leading toward a more <span class="highlight">gender-balanced</span> billionaire class?

---
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("BillionairesData.csv")
    df = df.dropna(subset=["country", "gender"])
    return df

df = load_data()

# Thay thế M/F bằng Male/Female
df['gender'] = df['gender'].replace({'M': 'Male', 'F': 'Female'})

# Select country
countries = df['country'].value_counts().index.tolist()
selected_country = st.selectbox("Select a country:", countries)

# Filter data by selected country
df_country = df[df['country'] == selected_country]

# Gender ratio
gender_counts = df_country['gender'].value_counts().reset_index()
gender_counts.columns = ['Gender', 'Count']
gender_counts['Percentage'] = (gender_counts['Count'] / gender_counts['Count'].sum() * 100).round(2)

# Donut chart
fig = px.pie(
    gender_counts,
    values='Count',
    names='Gender',
    hole=0.5,
    color_discrete_sequence=px.colors.qualitative.Set3,
    title=f"Gender Distribution of Billionaires in {selected_country}"
)
fig.update_traces(
    textinfo='percent+label',
    hoverinfo='label+percent+value',
    pull=[0.05] * len(gender_counts)
)
fig.update_layout(
    showlegend=True,
    margin=dict(t=50, b=20),
    height=500
)

# Display
st.plotly_chart(fig, use_container_width=True)
st.subheader(f"📊 Gender Statistics Table in {selected_country}")
st.dataframe(gender_counts)
