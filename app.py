import streamlit as st
import pandas as pd
import plotly.express as px

st.title("🧓 Phân tích Tài sản theo Nhóm Tuổi")

# Load dữ liệu
df = pd.read_csv("BillionairesData.csv", encoding="utf-8-sig")

# Đổi tên cho dễ hiểu
df.rename(columns={
    'finalWorth': 'NetWorth',
    'personName': 'Name',
    'age': 'Age',
}, inplace=True)

# Xử lý dữ liệu
df = df.dropna(subset=["Age", "NetWorth"])
df = df.sort_values(by="NetWorth", ascending=False).head(50)

# Tạo nhóm tuổi
def get_age_group(age):
    if age < 30:
        return "Under 30"
    elif age <= 50:
        return "31–50"
    elif age <= 70:
        return "51–70"
    else:
        return "Over 70"

df["Age Group"] = df["Age"].apply(get_age_group)

# Filter chọn nhóm tuổi
group_option = st.radio(
    "Chọn nhóm tuổi:",
    ["Under 30", "31–50", "51–70", "Over 70"]
)

# Lọc dữ liệu theo nhóm tuổi
filtered_df = df[df["Age Group"] == group_option]

# Biểu đồ
fig = px.bar(
    filtered_df,
    x="NetWorth",
    y="Name",
    orientation="h",
    color="NetWorth",
    title=f"Tài sản của các tỷ phú nhóm tuổi {group_option}",
    hover_data=["Age"]
)

st.plotly_chart(fig, use_container_width=True)

# Bảng dữ liệu
st.subheader(f"Danh sách tỷ phú nhóm {group_option}")
st.dataframe(filtered_df[["Name", "Age", "NetWorth"]].reset_index(drop=True))
