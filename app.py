import streamlit as st
import pandas as pd
import plotly.express as px

# Cấu hình giao diện rộng
st.set_page_config(layout="wide")
st.title("💰 Which Age Group Holds the Most Wealth?")

# Thêm nội dung vào website
st.markdown("""
### **How Does Age Impact Wealth?**

Wealth accumulation often peaks later in life, but certain individuals start amassing significant fortunes at much younger ages. **_Younger billionaires_** tend to dominate sectors like **_technology_**, **_social media_**, and **_e-commerce_**, which offer massive returns in relatively short timeframes. Many of today’s **_young billionaires_** made their fortunes by tapping into the rapid growth of these innovative industries.

On the other hand, **_older billionaires_** usually have **_diversified portfolios_** across sectors such as **_luxury goods_**, **_finance_**, and **_energy_**. Their vast fortunes have often been built over several decades through continuous investment and business development, establishing wealth that compounds over time.

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

# Gender Ratio of Billionaires Content
st.markdown("""
### **Gender Ratio of Billionaires**

In recent years, discussions about **_gender equality_** in business and wealth distribution have gained momentum. One area of interest is the **_gender ratio_** of billionaires globally. While the number of **_women billionaires_** is growing, the wealthiest individuals are still predominantly **_male_**. This **_gender disparity_** can be attributed to various factors, such as access to resources, societal expectations, and opportunities available in different industries.

### **Key Insights:**
- **_Male Billionaires_**: The majority of billionaires worldwide are **_men_**, particularly in industries such as **_finance_**, **_energy_**, and **_manufacturing_**, where historical male dominance has been strong. These sectors have traditionally been the backbone of wealth creation, leading to a higher concentration of male billionaires.
  
- **_Female Billionaires_**: Although fewer in number, **_female billionaires_** are making strides, especially in sectors such as **_retail_**, **_media_**, and **_fashion_**. Women who inherit wealth or have entrepreneurial ventures in consumer-driven sectors are increasingly appearing on the list of the wealthiest individuals.

- **Emerging Trends**: There has been a notable increase in the number of **_self-made female billionaires_**, particularly in **_technology_**, **_pharmaceuticals_**, and **_beauty industries_**. These sectors offer opportunities for innovation and growth, allowing women to break through traditional barriers.

### **Challenges and Opportunities for Women Billionaires:**
Despite the increasing number of female billionaires, women still face significant barriers to wealth accumulation compared to their male counterparts. These challenges include:
- Limited access to **_venture capital_** and business networks
- **_Gender biases_** in investment opportunities and leadership roles
- Societal expectations around the roles of women in both family and business

However, as societal norms evolve and more women enter the business world with groundbreaking ideas, the gap is slowly narrowing. **_Female billionaires_** like **_Oprah Winfrey_**, **_Kylie Jenner_**, and **_Francoise Bettencourt Meyers_** show that women can successfully create and grow massive fortunes.

---

### **Key Question:**
- **What is the gender distribution of billionaires by country?**
- **Which countries have a more balanced gender ratio among billionaires?**
""")

# Gender Ratio Visualization
# Load data for gender distribution by country
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
