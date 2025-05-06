import streamlit as st
import pandas as pd
import plotly.express as px

# Cấu hình giao diện rộng
st.set_page_config(layout="wide")
st.title("💰 Which Age Group Holds the Most Wealth?")

# Thêm nội dung vào website
st.markdown("""
This analysis showcases the top 10 billionaires by net worth, based on the 2023 dataset. The list highlights the wealthiest individuals across various age groups, ranked by their total wealth. The data reveals how these billionaires have accumulated massive fortunes, with younger billionaires benefitting from industries like technology and social media, while older billionaires often have diversified portfolios across multiple sectors. The top 10 showcase the diverse paths to achieving billionaire status, emphasizing how long-term growth, strategic investments, and industry dominance contribute to their financial success.

---

Key Insights:
- The <span style='color:#FFD700; font-weight:bold;'>61+</span> age group holds the <span style='color:#FFD700; font-weight:bold;'>largest</span> share of total billionaire net worth, underscoring the long-term nature of wealth accumulation.
- <span style='color:#FFD700; font-weight:bold;'>Net worth grows consistently with age</span>, with sharp increases observed <span style='color:#FFD700; font-weight:bold;'>after age 40</span>.
- <span style='color:#FFD700; font-weight:bold;'>Billionaires under 30 remain a minority</span>, contributing a small share despite media attention on young tech founders.
- <span style='color:#FFD700; font-weight:bold;'>Wealth consolidation typically peaks after age 50</span>, highlighting the power of compounding and strategic financial planning.
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
    title=f"Top 10 Billionaires by Net Worth in {selected_group} Age Group"
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
        top10[["Rank", "Name", "Age", "NetWorth"]].reset_index(drop=True),
        use_container_width=True
    )
