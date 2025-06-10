import plotly.express as px
import streamlit as st

st.markdown("Select an age group to view key insights.")

# Chuyển "Age" sang chuỗi để được xử lý như nhóm phân loại (categorical)
fig = px.bar(
    top10,
    x="Age",
    y="NetWorth",
    hover_name="Name",
    hover_data={"NetWorth": True, "Age": True, "Name": False},
    color=top10["Age"].astype(str),  # Phân nhóm rời rạc theo tuổi
    color_discrete_sequence=px.colors.qualitative.Set3  # Chọn bảng màu rõ rệt
)

fig.update_layout(
    xaxis_title="Age",
    yaxis_title="Net Worth (Billion $)",
    hoverlabel=dict(bgcolor="black", font_color="white", font_size=12),
    legend_title="Age"
)

col1, col2 = st.columns([3, 2])
with col1:
    st.plotly_chart(fig, use_container_width=True)
with col2:
    if selected_group == "All":
        st.subheader("📊 Top 10 Billionaires")
    else:
        st.subheader(f"📊 Top Billionaires in {selected_group} Group")

    st.dataframe(
        top10[["Rank", "Name", "Age", "NetWorth"]].reset_index(drop=True),
        use_container_width=True
    )

st.markdown("---")
