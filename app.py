import streamlit as st
import pandas as pd
import plotly.express as px

# Cấu hình giao diện rộng
st.set_page_config(layout="wide")
st.title("💰 Which Age Group Holds the Most Wealth?")

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
fig.update_layout(
    xaxis_title="Age",
    yaxis_title="Net Worth (Billion $)",
    hoverlabel=dict(bgcolor="white", font_size=12)
)

# Hiển thị biểu đồ và bảng song song
col1, col2 = st.columns([3, 2])

with col1:
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("📊 Top 10 Billionaires")
    st.dataframe(
        top10[["Name", "Age", "Gender", "NetWorth"]].reset_index(drop=True),
        use_container_width=True
    )
