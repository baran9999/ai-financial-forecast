import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load data
model_df = pd.read_csv("Model.csv")
assumptions_df = pd.read_csv("Assumptions.csv")
dashboard_df = pd.read_csv("Dashbaord.csv")  # yes, it's intentionally misspelled

st.set_page_config(page_title="AI Foresight", layout="wide")

st.title("📊 AI Foresight: Financial Forecast Dashboard")

# Sidebar sliders for assumptions
st.sidebar.header("Adjust Assumptions")

growth_rate = st.sidebar.slider(
    "Monthly Growth Rate (%)",
    0.0, 10.0,
    float(assumptions_df.iloc[0, 1]) * 100
)
churn_rate = st.sidebar.slider(
    "Churn Rate (%)",
    0.0, 10.0,
    float(assumptions_df.iloc[1, 1]) * 100
)
price = st.sidebar.number_input(
    "Subscription Price ($)",
    value=float(assumptions_df.iloc[2, 1])
)
variable_cost = st.sidebar.number_input(
    "Variable Cost per Subscriber ($)",
    value=float(assumptions_df.iloc[3, 1])
)
fixed_cost = st.sidebar.number_input(
    "Fixed Monthly Cost ($)",
    value=float(assumptions_df.iloc[4, 1])
)

# Dashboard KPIs
st.subheader("📈 Key Forecast Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("Total Revenue (2025)", f"${dashboard_df.iloc[0, 1]:,.0f}")
col2.metric("Total Profit (2025)", f"${dashboard_df.iloc[1, 1]:,.0f}")
col3.metric("Avg Subscribers", f"{int(dashboard_df.iloc[2, 1]):,}")

# Revenue + Profit Chart
st.subheader("📊 Monthly Revenue & Profit")

fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(model_df['Month'], model_df['Revenue'], label="Revenue")
ax.plot(model_df['Month'], model_df['Profit   '], label="Profit")
ax.set_xticks(model_df['Month'])
ax.set_xticklabels(model_df['Month'], rotation=45)
ax.legend()
st.pyplot(fig)

# Table
st.subheader("📄 Monthly Breakdown")
st.dataframe(model_df)

st.caption("Made for Life360 by Sharan Karunaagaran")
