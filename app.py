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
    </style>
""", unsafe_allow_html=True)


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


st.set_page_config(page_title="Life360 Forecast Copilot", layout="wide")

# --- Header ---
st.markdown("<h1 style='color:#7C3AED; font-size:32px;'>Forecast Copilot Dashboard</h1>", unsafe_allow_html=True)

# --- Sidebar ---
st.sidebar.header("Forecast Assumptions")
start_subs = st.sidebar.number_input("Starting Subscribers", value=50000)
growth = st.sidebar.slider("Monthly Growth Rate (%)", 0.0, 10.0, 5.0) / 100
churn = st.sidebar.slider("Churn Rate (%)", 0.0, 10.0, 5.0) / 100
price = st.sidebar.number_input("Subscription Price ($)", value=12.99)
var_cost = st.sidebar.number_input("Variable Cost per Subscriber ($)", value=1.25)
fixed_cost = st.sidebar.number_input("Fixed Monthly Cost ($)", value=500000.0)

# --- Forecast Simulation ---
df = simulate_forecast(start_subs, growth, churn, price, var_cost, fixed_cost)

# --- KPI Metrics ---
st.markdown("<div style='background-color: #EDE9FE; padding: 1rem; border-radius: 10px; margin-top: 1rem;'>", unsafe_allow_html=True)
st.subheader("Key Financial Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("Total Revenue", f"${df['Revenue'].sum():,.0f}")
col2.metric("Total Profit", f"${df['Profit'].sum():,.0f}")
col3.metric("Ending Subscribers", f"{int(df['Subscribers'].iloc[-1]):,}")
st.markdown("</div>", unsafe_allow_html=True)

# --- Chart ---
st.markdown("<div style='background-color: #F9FAFB; padding: 1rem; border-radius: 10px; margin-top: 1rem;'>", unsafe_allow_html=True)
st.subheader("Monthly Revenue and Profit")
fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(df["Month"], df["Revenue"], label="Revenue", color="#7C3AED")
ax.plot(df["Month"], df["Profit"], label="Profit", color="#4B5563")
plt.xticks(rotation=45)
ax.legend()
st.pyplot(fig)
st.markdown("</div>", unsafe_allow_html=True)

# --- Data Table ---
st.markdown("<div style='margin-top: 1rem;'>", unsafe_allow_html=True)
st.subheader("Monthly Forecast Table")
formatted_df = df.copy()
dollar_cols = ["Revenue", "Variable Costs", "Fixed Costs", "Total Costs", "Profit"]
for col in dollar_cols:
    formatted_df[col] = formatted_df[col].map("${:,.2f}".format)
st.dataframe(formatted_df)
st.markdown("</div>", unsafe_allow_html=True)

# --- AI Forecast Copilot ---
st.markdown("<div style='margin-top: 2rem;'>", unsafe_allow_html=True)
st.subheader("AI Forecast Copilot")

user_prompt = st.text_input("Ask a forecasting question (e.g. 'How would an 8% churn affect 2025 net profit?')")

if user_prompt:
    with st.spinner("Generating AI insight..."):
        try:
            prompt = f"""
            You're an internal financial forecasting assistant at Life360.
            Use the current model assumptions and business context to deliver sharp, executive-ready insights.

            Key assumptions:
            - Starting Subscribers: {start_subs}
            - Monthly Growth Rate: {growth:.2%}
            - Monthly Churn Rate: {churn:.2%}
            - Subscription Price: ${price}
            - Variable Cost per Subscriber: ${var_cost}
            - Fixed Monthly Cost: ${fixed_cost}

            Company context: Life360 is a location-based service platform generating revenue primarily from subscription services. The goal is to optimize unit economics, grow subscriber base, and expand profitability. Use this lens to assess the question.

            Question: {user_prompt}

            Keep it brief, focused, and aligned with internal Life360 financial reporting tone.
            """

            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a financial forecasting assistant trained on Life360 context."},
                    {"role": "user", "content": prompt}
                ]
            )

            st.success(response.choices[0].message.content)

        except openai.RateLimitError:
            st.error("Rate limit reached. Please try again shortly.")
        except Exception as e:
            st.error(f"An error occurred: {e}")

st.markdown("</div>", unsafe_allow_html=True)

# --- Footer ---
st.markdown("""
    <hr style="margin-top: 30px;">
    <div style='text-align: right; font-size: 13px; color: #999999;'>
        For Life360 — made by Sharan Karunaagaran
    </div>
""", unsafe_allow_html=True)
