import streamlit as st
import pandas as pd
import plotly.express as px

# Đọc file CSV
billionaires = pd.read_csv('BillionairesData.csv', encoding='utf-8-sig')

# Chọn top 50 theo giá trị ròng
billionaires = billionaires.sort_values(by='finalWorth', ascending=False).head(50)

# Nhóm tuổi
def age_group(age):
    if age < 30:
        return 'Dưới 30'
    elif 30 <= age <= 50:
        return '31-50'
    elif 51 <= age <= 70:
        return '51-70'
    else:
        return 'Trên 70'

billionaires['Age Group'] = billionaires['age'].apply(age_group)

# Biểu đồ
fig = px.bar(
    billionaires,
    x='finalWorth',
    y='age',
    color='age',
    orientation='h',
    hover_data={'Person': True, 'FinalWorth': ':.2f'},
    labels={'finalWorth': 'Giá trị ròng (tỷ USD)', 'age': 'Nhóm tuổi'},
    title='Top 50 Tỷ phú theo nhóm tuổi và giá trị ròng'
)

# Tổng hợp bảng
age_group_summary = (
    billionaires.groupby('age')
    .agg(
        So_Top=('Person', 'count'),
        Tong_Gia_Tri_Rong=('finalWorth', 'sum')
    )
    .reset_index()
)

# Hiển thị trên Streamlit
st.title("Top 50 Tỷ phú theo nhóm tuổi - Dữ liệu 2023")
st.plotly_chart(fig, use_container_width=True)
st.subheader("Bảng thống kê")
st.dataframe(age_group_summary)
