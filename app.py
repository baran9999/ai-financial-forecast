import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import openai

client = openai.OpenAI(api_key=st.secrets["openai"]["api_key"])

# --- Forecast Function ---
def simulate_forecast(start_subs, growth, churn, price, var_cost, fixed_cost):
    months = pd.date_range("2025-01-01", periods=12, freq='MS')
    data = []
    subs = start_subs

    for m in months:
        new_subs = subs * growth
        churned_subs = subs * churn
        subs = subs + new_subs - churned_subs
        revenue = subs * price
        variable_costs = subs * var_cost
        total_costs = variable_costs + fixed_cost
        profit = revenue - total_costs

        data.append({
            "Month": m.strftime("%Y-%m"),
            "Subscribers": int(subs),
            "Revenue": revenue,
            "Variable Costs": variable_costs,
            "Fixed Costs": fixed_cost,
            "Total Costs": total_costs,
            "Profit": profit
        })

    return pd.DataFrame(data)

# --- Sidebar Inputs ---
st.sidebar.header("Forecast Assumptions")
start_subs = st.sidebar.number_input("Starting Subscribers", value=50000)
growth = st.sidebar.slider("Monthly Growth Rate (%)", 0.0, 10.0, 5.0) / 100
churn = st.sidebar.slider("Churn Rate (%)", 0.0, 10.0, 5.0) / 100
price = st.sidebar.number_input("Subscription Price ($)", value=12.99)
var_cost = st.sidebar.number_input("Variable Cost per Subscriber ($)", value=1.25)
fixed_cost = st.sidebar.number_input("Fixed Monthly Cost ($)", value=500000.0)

# --- Generate Forecast ---
df = simulate_forecast(start_subs, growth, churn, price, var_cost, fixed_cost)

# --- Brand Styling ---
st.markdown("""
    <style>
        /* Purple slider and thumb */
        .stSlider > div[data-baseweb="slider"] > div {
            color: #7C3AED !important;
        }
        .stSlider > div[data-baseweb="slider"] span {
            background-color: #7C3AED !important;
        }

        /* Sidebar background */
        section[data-testid="stSidebar"] {
            background-color: #F9F5FF;
            padding: 2rem 1rem 1rem 1rem;
        }

        /* Sidebar header text */
        .sidebar .sidebar-content h1,
        .sidebar .sidebar-content h2,
        .sidebar .sidebar-content h3 {
            color: #7C3AED;
        }

        /* Inputs and labels */
        .stNumberInput label, .stSlider label {
            color: #1F2937 !important;
            font-weight: 500;
        }

        /* Input boxes */
        .stNumberInput input {
            background-color: white;
            border: 1px solid #D1D5DB;
            border-radius: 6px;
        }

        /* Limit chart width tighter */
        .chart-container {
            max-width: 380px;
            margin: auto;
        }

        /* Shrink image padding */
        .element-container iframe, .element-container canvas {
            max-height: 200px !important;
        }

        /* Table should be full width */
        .block-container {
            padding: 1rem;
        }
    </style>
""", unsafe_allow_html=True)

# --- Chart Section with Expandable Toggle ---
st.markdown("<div class='chart-container' style='background-color: #F9FAFB; padding: 1rem; border-radius: 10px; margin-top: 1rem;'>", unsafe_allow_html=True)
st.subheader("Monthly Revenue and Profit")

with st.expander("Click to view chart"):
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(df["Month"], df["Revenue"], label="Revenue", color="#7C3AED")
    ax.plot(df["Month"], df["Profit"], label="Profit", color="#4B5563")
    plt.xticks(rotation=45)
    ax.legend()
    st.pyplot(fig)

st.markdown("</div>", unsafe_allow_html=True)

# --- Forecast Table ---
st.markdown("<div style='margin-top: 1rem;'>", unsafe_allow_html=True)
st.subheader("Monthly Forecast Table")
formatted_df = df.copy()
dollar_cols = ["Revenue", "Variable Costs", "Fixed Costs", "Total Costs", "Profit"]
for col in dollar_cols:
    formatted_df[col] = formatted_df[col].map("${:,.2f}".format)
st.dataframe(formatted_df, use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)
