import streamlit as st
import pandas as pd
import plotly.express as px

st.title("💰 Which Age Group Holds the Most Wealth?")

# Load dữ liệu
df = pd.read_csv("BillionairesData.csv", encoding="utf-8-sig")

# Chuẩn hóa tên cột
df.rename(columns={
    'finalWorth': 'NetWorth',
    'personName': 'Name',
    'age': 'Age',
    'gender': 'Gender'
}, inplace=True)

# Loại bỏ dữ liệu thiếu
df = df.dropna(subset=["Age", "NetWorth", "Gender"])

# Nhóm tuổi theo yêu cầu
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

# Selectbox chọn nhóm tuổi
age_groups = ["All", "Under 20", "21–30", "31–40", "41–50", "51–60", "61+"]
selected_group = st.selectbox("Select Age Group", age_groups)

# Lọc theo nhóm tuổi nếu chọn khác "All"
if selected_group != "All":
    df = df[df["Age Group"] == selected_group]

# Top 10 tỷ phú theo giá trị ròng
top_10 = df.sort_values(by="NetWorth", ascending=False).head(10)

# Biểu đồ
fig = px.bar(
    top_10,
    x="Age",
    y="NetWorth",
    orientation="v",
    hover_name="Name",
    hover_data={"NetWorth": True, "Name": False},
    color="Age",
    title="Top 10 Billionaires by Age and Net Worth"
)
fig.update_layout(xaxis_title="Age", yaxis_title="Net Worth (Billion $)")

st.plotly_chart(fig, use_container_width=True)

# Bảng dữ liệu
st.subheader("Top 10 Billionaires (Filtered by Age Group)")
st.dataframe(top_10[["Name", "Age", "NetWorth", "Gender"]].reset_index(drop=True))
