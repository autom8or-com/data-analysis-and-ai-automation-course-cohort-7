"""
Streamlit Example App — Week 8 Thursday
Olist Order Analysis Dashboard

Run with: streamlit run streamlit_example.py
Requires: pandas, streamlit
"""

import streamlit as st
import pandas as pd

# Page configuration
st.set_page_config(page_title="Olist Orders", layout="wide")

# Title
st.title("📊 Olist Order Analysis Dashboard")
st.write("Explore order patterns from the Brazilian Olist e-commerce platform (2016–2018)")

# Sidebar
st.sidebar.title("Navigation")
page = st.sidebar.radio("Select analysis:", ["Overview", "By State", "By Status"])

# Load data (in production, load from Google Drive or database)
@st.cache_data
def load_data():
    orders = pd.read_csv("olist_orders_dataset.csv")
    customers = pd.read_csv("olist_customers_dataset.csv")
    merged = orders.merge(customers, on="customer_id", how="left")
    return merged

data = load_data()

# Page 1: Overview
if page == "Overview":
    st.header("📈 Overview")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Orders", f"{len(data):,}")
    with col2:
        delivered = len(data[data['order_status'] == 'delivered'])
        st.metric("Delivered", f"{delivered:,}")
    with col3:
        cancelled = len(data[data['order_status'] == 'cancelled'])
        st.metric("Cancelled", f"{cancelled:,}")
    
    st.subheader("Orders by Status")
    status_counts = data['order_status'].value_counts()
    st.bar_chart(status_counts)

# Page 2: By State
elif page == "By State":
    st.header("🗺️ Orders by State")
    
    state_counts = data['customer_state'].value_counts()
    st.bar_chart(state_counts.head(10))
    
    st.subheader("Top 10 States")
    st.table(state_counts.head(10).rename("Order Count"))

# Page 3: By Status
else:  # page == "By Status"
    st.header("🎯 Orders by Status")
    
    status_breakdown = data['order_status'].value_counts()
    st.pie_chart(status_breakdown)
    
    st.subheader("Status Breakdown")
    for status, count in status_breakdown.items():
        st.write(f"**{status.title()}**: {count:,} orders ({count/len(data)*100:.1f}%)")

# Footer
st.divider()
st.caption("Data: Olist E-commerce Dataset (2016–2018) | PORA Academy Cohort 7")
