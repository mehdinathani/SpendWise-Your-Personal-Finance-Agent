# SpendWise 🔥 - Streamlit Frontend (app.py)
# --------------------------------------------------
import streamlit as st
from tools import ExpenseLookupTool
from agents import route_query
from guardrails import check_input_guardrail, check_output_guardrail
from model import SpendingSummary, UserQuery
import pandas as pd
import random

# -------------- Dummy Actual Spend Data --------------
ACTUAL_SPENDS = {
    "Food": random.randint(3000, 8000),
    "Transport": random.randint(1000, 4000),
    "Entertainment": random.randint(2000, 6000),
    "Utilities": random.randint(2500, 5000),
    "Savings": random.randint(5000, 10000)
}

# -------------- Streamlit Layout --------------
st.set_page_config(page_title="SpendWise 🔥", layout="wide")
st.title("💸 SpendWise: Your Gen-Z Finance Copilot")

# Sidebar Inputs
st.sidebar.header("🎛️ Input Your Budget")
user_name = st.sidebar.text_input("🙋‍♂️ Your Name", "Mehdi")
budget_food = st.sidebar.number_input("🍔 Food Budget", value=5000)
budget_transport = st.sidebar.number_input("🚌 Transport Budget", value=2000)
budget_entertainment = st.sidebar.number_input("🎮 Entertainment Budget", value=3000)
budget_utilities = st.sidebar.number_input("💡 Utilities Budget", value=3500)
budget_savings = st.sidebar.number_input("🏦 Savings Goal", value=8000)

user_query = st.sidebar.text_area("💬 Ask anything...", "How much did I spend on food this month?")
analyze_btn = st.sidebar.button("🔍 Analyze")

# Collect Budget Inputs
budgets = {
    "Food": budget_food,
    "Transport": budget_transport,
    "Entertainment": budget_entertainment,
    "Utilities": budget_utilities,
    "Savings": budget_savings
}

# Result Placeholders
dashboard_col, result_col = st.columns([1, 3])

if analyze_btn:
    st.toast("🧠 Thinking... Hold tight!", icon="🔄")

    # Step 1: Input Guardrail
    guardrail_msg = check_input_guardrail(user_query, budgets)
    if guardrail_msg:
        st.error(f"🚫 {guardrail_msg}")
    else:
        # Step 2: Query Routing & Tool Execution
        summary: SpendingSummary = ExpenseLookupTool().run(budgets, ACTUAL_SPENDS)
        advice = route_query(UserQuery(name=user_name, query=user_query, context=summary))

        # Step 3: Output Guardrail
        output_msg = check_output_guardrail(advice)

        # Step 4: Tracing Dashboard
        with dashboard_col:
            st.subheader("📟 Agent/Tool/Guardrail Tracker")
            st.markdown("""
            <div style='display: flex; gap: 8px;'>
                <span style='background-color: lightgreen; padding: 4px 8px; border-radius: 5px;'>Agent: BudgetAdvisor</span>
                <span style='background-color: lightgreen; padding: 4px 8px; border-radius: 5px;'>Tool: DBLookupTool</span>
                <span style='background-color: {input_color}; padding: 4px 8px; border-radius: 5px;'>Guardrail: Input</span>
                <span style='background-color: {output_color}; padding: 4px 8px; border-radius: 5px;'>Guardrail: Output</span>
            </div>
            """.format(
                input_color="grey" if guardrail_msg is None else "lightgreen",
                output_color="grey" if output_msg is None else "orange"
            ), unsafe_allow_html=True)

        # Step 5: Output Rendering
        with result_col:
            st.subheader("📊 Spending Summary")
            df = pd.DataFrame({
                "Category": list(budgets.keys()),
                "Budgeted": list(budgets.values()),
                "Spent": [ACTUAL_SPENDS[k] for k in budgets.keys()]
            })
            st.dataframe(df, use_container_width=True)

            st.subheader("💬 Smart Advice")
            st.info(advice)

            if output_msg:
                st.warning(f"⚠️ {output_msg}")

            # Export Button
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("📤 Download CSV", csv, "spending_summary.csv", "text/csv")
