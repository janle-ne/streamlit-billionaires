import streamlit as st
import pandas as pd
import plotly.express as px

# Cấu hình giao diện rộng
st.set_page_config(layout="wide")
st.title("💰 Which Age Group Holds the Most Wealth?")

# Thêm nội dung vào website
st.markdown("""
<div style="background-color:#fdf6e3;padding:1rem;border-radius:10px">
<h3><b>How Does Age Impact Wealth?</b></h3>
<p>
Wealth accumulation often peaks later in life, but certain individuals start amassing significant fortunes at much younger ages. 
<span style="background-color:#228B22;color:white;border-radius:4px;padding:2px 6px">Younger billionaires</span> tend to dominate sectors like 
<span style="background-color:#228B22;color:white;border-radius:4px;padding:2px 6px">technology</span>, <span style="background-color:#228B22;color:white;border-radius:4px;padding:2px 6px">social media</span>, and 
<span style="background-color:#228B22;color:white;border-radius:4px;padding:2px 6px">e-commerce</span>, which offer massive returns in relatively short timeframes.
</p>
<p>
On the other hand, <span style="background-color:#228B22;color:white;border-radius:4px;padding:2px 6px">older billionaires</span> usually have 
<span style="background-color:#228B22;color:white;border-radius:4px;padding:2px 6px">diversified portfolios</span> across sectors such as 
<span style="background-color:#228B22;color:white;border-radius:4px;padding:2px 6px">luxury goods</span>, <span style="background-color:#228B22;color:white;border-radius:4px;padding:2px 6px">finance</span>, and 
<span style="background-color:#228B22;color:white;border-radius:4px;padding:2px 6px">energy</span>. Their vast fortunes have often been built over several decades through continuous investment and business development.
</p>
<hr>
<h4><b>Key Questions:</b></h4>
<ul>
<li><b>Which Age Group Holds the Most Wealth?</b></li>
</ul>
</div>
""", unsafe_allow_html=True)

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
        bgcolor="black",
        font_color="white",
        font_size=12
    )
)

# Hiển thị biểu đồ và bảng song song
col1, col2 = st.columns([3, 2])

with col1:
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("📊 Top 10 Billionaires")
    st.dataframe(
        top10[["Rank", "Name", "Age", "Gender", "NetWorth"]].reset_index(drop=True),
        use_container_width=True
    )

# Phần gender chart
st.markdown("""
---
<h2 style="margin-top:2rem">🌍 Gender Ratio of Billionaires by Country</h2>
<div style="background-color:#fdf6e3;padding:1rem;border-radius:10px">
<p>
The distribution of billionaire wealth also reveals gender disparities. 
While men still dominate the billionaire list globally, a growing number of 
<span style="background-color:#228B22;color:white;border-radius:4px;padding:2px 6px">female billionaires</span> are emerging, especially in sectors like fashion, inheritance, and family business.
</p>
<p>
Exploring gender distribution by country helps highlight both 
<span style="background-color:#228B22;color:white;border-radius:4px;padding:2px 6px">economic</span> and 
<span style="background-color:#228B22;color:white;border-radius:4px;padding:2px 6px">cultural</span> factors that may influence wealth-building opportunities.
</p>
</div>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("BillionairesData.csv")
    df = df.dropna(subset=["country", "gender"])
    df["gender"] = df["
