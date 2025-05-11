import streamlit as st
import pandas as pd
import plotly.express as px
from annotated_text import annotated_text

def show():
    st.title("💰 Which Age Group Holds the Most Wealth?")

    st.markdown(""" 
    This analysis showcases the top 10 billionaires by net worth, based on the 2023 dataset. The list highlights the wealthiest individuals across various age groups, ranked by their total wealth. The data reveals how these billionaires have accumulated massive fortunes, with younger billionaires benefitting from industries like technology and social media, while older billionaires often have diversified portfolios across multiple sectors. The top 10 showcase the diverse paths to achieving billionaire status, emphasizing how long-term growth, strategic investments, and industry dominance contribute to their financial success.

    ---
    """, unsafe_allow_html=True)

    # Create an empty container
    single_column = st.empty()

    # Load data
    df = pd.read_csv("Billionaires Statistics Dataset.csv", encoding="utf-8-sig")

    # Normalize column names
    df.rename(columns={
        'finalWorth': 'NetWorth',
        'personName': 'Name',
        'age': 'Age',
        'gender': 'Gender'
    }, inplace=True)

    df = df.dropna(subset=["Age", "NetWorth", "Gender"])

    # Define the age group
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

    # Filter by age group
    age_groups = ["All", "Under 20", "21–30", "31–40", "41–50", "51–60", "61+"]
    selected_group = st.selectbox("🎯 Select Age Group", age_groups)

    filtered_df = df.copy()
    if selected_group != "All":
        filtered_df = df[df["Age Group"] == selected_group]

    # Top 10
    top10 = filtered_df.sort_values(by="NetWorth", ascending=False).head(10)
    top10['Rank'] = top10['NetWorth'].rank(ascending=False, method='min')

    # Key Insights based on Age Group
    key_insights = {
        "Under 20":"✅ **Under 20 Age Group**\nBillionaires under 20 are a rare and unique group, often driven by innovation in technology, gaming, or even social media platforms. Despite their youth, many of these individuals have rapidly built their fortunes through successful startups, viral online businesses, or early investments in emerging sectors like cryptocurrency. While they represent a small portion of the total billionaire wealth, their potential for future growth is immense. The under-20 billionaires are early adopters of digital technologies and demonstrate the growing role of youth in wealth creation.",
        "21–30": "✅ **21-30 Age Group**\nThis youngest billionaire group represents a small portion of total wealth but signals a promising rise of tech-savvy entrepreneurs. Many in this age group built their fortune from innovative startups, cryptocurrency, or software platforms. Although their combined net worth is significantly lower than older groups, the pace at which some members accumulated wealth is noteworthy. This group reflects the growing impact of digital innovation on wealth creation.",
        "31–40": "✅ **31-40 Age Group**\nBillionaires aged 31–40 begin to show more influence on the overall wealth landscape. With more experience and maturing businesses, many of them scaled startups into global enterprises. Technology remains the dominant sector here, with a few notable figures making up large portions of this group's net worth. While still behind older groups in total wealth, they show strong upward momentum.",
        "31–40": "✅ **31-40 Age Group**\nBillionaires aged 31–40 begin to show more influence on the overall wealth landscape. With more experience and maturing businesses, many of them scaled startups into global enterprises. Technology remains the dominant sector here, with a few notable figures making up large portions of this group's net worth. While still behind older groups in total wealth, they show strong upward momentum.",
        "41–50": "✅ **41-50 Age Group**\nThis age group marks a transition toward wealth consolidation. Many individuals here are seasoned entrepreneurs or executives in both tech and traditional industries. Compared to younger age brackets, the total net worth sees a noticeable increase, as businesses founded earlier now yield substantial returns. The wealth gap between this group and those in their 30s highlights how time significantly contributes to financial growth.",
        "51–60": "✅ **51-60 Age Group**\nWith decades of experience, billionaires in their 50s often have diversified portfolios and stable positions in established industries. This group begins to approach the peak in terms of wealth accumulation. Many are long-time business owners or key shareholders in multinational firms. Their wealth reflects a combination of strategic investments, legacy holdings, and accumulated growth over time.",
        "61+": "✅ **60+ Age Group**\nThis is the most affluent age group, holding the largest share of total billionaire wealth. These individuals have had the most time to grow their assets, often inheriting businesses or building empires over multiple decades. Their presence is strongest in sectors like finance, energy, and real estate. The data shows a clear link between age and net worth, with this group showcasing the long-term effect of compounding wealth and stability."
    }

    # Display Key Insights for the selected age group
    if selected_group != "All":
        st.markdown(key_insights.get(selected_group, ""))
    else:
        st.markdown("Select an age group to view key insights.")

    # Plot the graph
    fig = px.bar(
        top10,
        x="Age",
        y="NetWorth",
        hover_name="Name",
        hover_data={"NetWorth": True, "Age": True, "Name": False},
        color="Age",
        title=f"Top 10 Billionaires by Net Worth in {selected_group} Age Group"
    )
    fig.update_layout(
        xaxis_title="Age",
        yaxis_title="Net Worth (Billion $)",
        hoverlabel=dict(bgcolor="black", font_color="white", font_size=12)
    )

    # Display the graph and table
    col1, col2 = st.columns([3, 2])
    with col1:
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        if selected_group == "All":
            st.subheader("📊 Top 10 Billionaires")
        else:
            st.subheader(f"📊 Top Billionaires in {selected_group} Group")  # Fixed the typo here

        st.dataframe(
            top10[["Rank", "Name", "Age", "NetWorth"]].reset_index(drop=True),
            use_container_width=True
        )
