import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import openai

client = openai.OpenAI(api_key=st.secrets["openai"]["api_key"])

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
