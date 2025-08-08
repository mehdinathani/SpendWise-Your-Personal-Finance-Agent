
# import sys
# import os
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agents import Agent
from guardrails import check_user_input_guardrail, check_agent_output_guardrail
from tools.tools import analyze_spending




# Define the agent with tool
BudgetAdvisor = Agent(
    name="Budget Advisor Agent",
    tools=[analyze_spending],
    instructions="You are a Gen-Z friendly financial coach. For any budget or spending query, use the analyze_spending tool to check the user's budget and actuals from the context. Be concise, empathetic, and informal.",
    input_guardrails=[check_user_input_guardrail],
    output_guardrails=[check_agent_output_guardrail]
)

