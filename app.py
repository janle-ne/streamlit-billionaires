import streamlit as st
import pandas as pd
import plotly.express as px

# Cấu hình giao diện rộng
st.set_page_config(layout="wide")
st.title("💰 Which Age Group Holds the Most Wealth?")

# Thêm nội dung vào website
st.markdown("""
### **How Does Age Impact Wealth?**

Wealth accumulation often peaks later in life, but certain individuals start amassing significant fortunes at much younger ages. **Younger billionaires** tend to dominate sectors like **technology**, **social media**, and **e-commerce**, which offer massive returns in relatively short timeframes. Many of today’s **young billionaires** made their fortunes by tapping into the rapid growth of these innovative industries.

On the other hand, **older billionaires** usually have **diversified portfolios** across sectors such as **luxury goods**, **finance**, and **energy**. Their vast fortunes have often been built over several decades through continuous investment and business development, establishing wealth that compounds over time.

---

### **Key Questions:**
- **Which Age Group Holds the Most Wealth?**
""")

# Tải dữ liệu
df = pd.read_csv("BillionairesData.csv", encoding="utf-8-sig")

# Chuẩn hóa cột
df.rename(columns={
    'finalWorth': 'NetWorth',
    'personName': 'Name',
    'age': 'Age',
    'gender': 'Gender'
}, inplace=True)

# Xóa dòng thiếu dữ liệu quan trọng
df = df.dropna(subset=["Age", "NetWorth", "Gender"])

# Nhóm tuổi tùy chỉnh
def get_age_group(age):
    if age <= 20:
        return "Under 20"
    elif age <= 30:
        return "21–30"
    elif age <= 40:
        return "31–40"
    elif age <= 50:
        return "41–50"
    elif age <= 60:
        return "51–60"
    else:
        return "61+"

df["Age Group"] = df["Age"].apply(get_age_group)

# Bộ lọc nhóm tuổi
age_groups = ["All", "Under 20", "21–30", "31–40", "41–50", "51–60", "61+"]
selected_group = st.selectbox("🎯 Select Age Group", age_groups)

# Lọc dữ liệu theo nhóm tuổi
filtered_df = df.copy()
if selected_group != "All":
    filtered_df = df[df["Age Group"] == selected_group]

# Chọn top 10 theo tài sản
top10 = filtered_df.sort_values(by="NetWorth", ascending=False).head(10)

# Thêm cột xếp hạng
top10['Rank'] = top10['NetWorth'].rank(ascending=False, method='min')

# Biểu đồ
fig = px.bar(
    top10,
    x="Age",
    y="NetWorth",
    hover_name="Name",
    hover_data={"NetWorth": True, "Age": True, "Name": False},
    color="Age",
    title="Top 10 Billionaires by Net Worth in Selected Age Group"
)

# Cập nhật hover label
fig.update_layout(
    xaxis_title="Age",
    yaxis_title="Net Worth (Billion $)",
    hoverlabel=dict(
        bgcolor="black",  # Nền hover là màu đen
        font_color="white",  # Chữ trong hover là màu trắng
        font_size=12  # Kích thước chữ
    )
)

# Hiển thị biểu đồ và bảng song song
col1, col2 = st.columns([3, 2])

with col1:
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("📊 Top 10 Billionaires")
    # Hiển thị bảng có thêm cột Rank
    st.dataframe(
        top10[["Rank", "Name", "Age", "NetWorth"]].reset_index(drop=True),
        use_container_width=True
    )
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
