import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import openai

# Load OpenAI API key securely
client = openai.OpenAI(api_key=st.secrets["openai"]["api_key"])

# ---------------------------
# Forecast Simulation Logic
# ---------------------------
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

# ---------------------------
# Streamlit UI
# ---------------------------
st.set_page_config(page_title="AI Forecast Copilot", layout="wide")
st.title("🤖 AI Foresight Copilot — Dynamic Financial Forecasting")

# Sidebar sliders
st.sidebar.header("📊 Adjust Assumptions")
start_subs = st.sidebar.number_input("Starting Subscribers", value=50000)
growth = st.sidebar.slider("Monthly Growth Rate (%)", 0.0, 10.0, 5.0) / 100
churn = st.sidebar.slider("Churn Rate (%)", 0.0, 10.0, 5.0) / 100
price = st.sidebar.number_input("Subscription Price ($)", value=12.99)
var_cost = st.sidebar.number_input("Variable Cost per Sub ($)", value=1.25)
fixed_cost = st.sidebar.number_input("Fixed Monthly Cost ($)", value=500000.0)

# Run simulation
df = simulate_forecast(start_subs, growth, churn, price, var_cost, fixed_cost)

# KPI Metrics
st.subheader("📈 Key Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("Total Revenue", f"${df['Revenue'].sum():,.0f}")
col2.metric("Total Profit", f"${df['Profit'].sum():,.0f}")
col3.metric("End Subscribers", f"{int(df['Subscribers'].iloc[-1]):,}")

# Chart
st.subheader("📊 Monthly Revenue & Profit")
fig, ax = plt.subplots()
ax.plot(df["Month"], df["Revenue"], label="Revenue")
ax.plot(df["Month"], df["Profit"], label="Profit")
plt.xticks(rotation=45)
ax.legend()
st.pyplot(fig)

# Data Table
st.subheader("📄 Monthly Breakdown")
st.dataframe(df)

# ---------------------------
# AI Forecast Copilot
# ---------------------------
st.subheader("🧠 AI Forecast Copilot")

user_prompt = st.text_input("Ask me something about the forecast (e.g. 'What happens if churn is 8%?')")

if user_prompt:
    with st.spinner("Thinking like a financial analyst..."):
        try:
            prompt = f"""
            You are an AI financial analyst. The user is adjusting assumptions in a subscription forecast model.

            Use this current data to answer:
            - Starting Subscribers: {start_subs}
            - Monthly Growth Rate: {growth:.2%}
            - Monthly Churn Rate: {churn:.2%}
            - Price: ${price}
            - Variable Cost per Sub: ${var_cost}
            - Fixed Cost per Month: ${fixed_cost}

            The user asked: {user_prompt}

            Respond with a clear financial insight or scenario projection, based on those numbers.
            """

            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You're a financial forecasting assistant."},
                    {"role": "user", "content": prompt}
                ]
            )

            st.success(response.choices[0].message.content)

        except openai.RateLimitError:
            st.error("🚫 You're hitting the OpenAI rate limit. Please wait a bit and try again.")
        except Exception as e:
            st.error(f"❌ Something went wrong: {e}")

st.caption("Made for Life360 ✨ by Sharan Karunaagaran")
