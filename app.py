import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt

# Page configuration
st.set_page_config(page_title="E-Commerce Customer Segmentation", layout="wide")

st.title("🛒 E-Commerce Customer Segmentation & RFM Dashboard")
st.write("An interactive web app built using Python, K-Means Clustering, and the Olist E-Commerce dataset.")

@st.cache_data
def load_data():
    # Load your pre-processed or original data logic here
    # For demonstration, let's load a sample or summary of your RFM segments
    data = {
        'Segment': ['Recent Customers', 'Inactive / Churned', 'Loyal Repeaters', 'VIP Big Spenders'],
        'Customer_Count': [51886, 38378, 2883, 2273],
        'Avg_Recency_Days': [133.52, 393.69, 226.18, 244.35],
        'Avg_Monetary_Spend': [113.60, 114.48, 243.05, 1145.31]
    }
    return pd.DataFrame(data)

df_summary = load_data()

# Sidebar options
st.sidebar.header("Navigation")
option = st.sidebar.selectbox("Choose a view:", ["Overview & Segments", "Explore Metrics"])

if option == "Overview & Segments":
    st.header("Customer Segment Distribution")
    st.write("Here is the breakdown of our customer base grouped using K-Means Clustering ($k=4$):")
    
    # Display table
    st.dataframe(df_summary, use_container_width=True)
    
    # Display bar chart
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(data=df_summary, x='Segment', y='Customer_Count', palette='viridis', hue='Segment', legend=False, ax=ax)
    plt.xticks(rotation=15)
    plt.title("Customer Count per Segment")
    st.pyplot(fig)

elif option == "Explore Metrics":
    st.header("Deep Dive into Segment Behavior")
    selected_segment = st.selectbox("Select a Segment to inspect:", df_summary['Segment'].unique())
    
    row = df_summary[df_summary['Segment'] == selected_segment].iloc[0]
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Total Customers", value=f"{row['Customer_Count']:,}")
    with col2:
        st.metric(label="Average Monetary Spend ($)", value=f"${row['Avg_Monetary_Spend']:,.2f}")
        
    st.write(f"**Insights for {selected_segment}:**")
    if selected_segment == 'VIP Big Spenders':
        st.info("This is your highest-value cohort. They spend significantly more per user and should be prioritized for exclusive perks.")
    elif selected_segment == 'Inactive / Churned':
        st.warning("This group hasn't purchased in a long time. Consider launching a targeted automated win-back email campaign.")
    elif selected_segment == 'Loyal Repeaters':
        st.success("Consistent buyers who shop more than once. Great candidates for loyalty or referral programs.")
    else:
        st.write("Recent one-off shoppers who form the bulk of your active funnel.")

        