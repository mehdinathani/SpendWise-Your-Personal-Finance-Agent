
# import sys
# import os
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agents import Agent, function_tool, Runner, RunContextWrapper
from tools.tools import ExpenseLookupTool
from models.model import BudgetContext
from llm7config import config

# Tool decorated for LLM tool use (even though it's hardcoded/mock for now)
@function_tool
async def analyze_spending(wrapper: RunContextWrapper[BudgetContext]) -> str:
    """Provide advice based on user's budget and actuals."""
    ctx = wrapper.context
    food_budget = ctx.budgets.get("Food", 0)
    food_actual = ctx.actuals.get("Food", 0)

    if food_actual > food_budget:
        return f"You are overspending on Food! Budget: {food_budget}, Actual: {food_actual}"
    return "Your spending is within budget."


# Define the agent with tool
BudgetAdvisor = Agent(
    name="Budget Advisor Agent",
    tools=[analyze_spending],
    instructions="""You are a Gen-Z friendly financial coach. Be helpful, concise, and informal.
                    You are given user spending data. Provide smart and empathetic advice."""
)



# # Function to route the query to the agent

# def route_query(user_input: UserQuery) -> str:
#     # Run the agent with the summary as tool input
#     result = runner.run(
#         BudgetAdvisor,
#         input=user_input.query,
#         tools=[summarize_budget]
        
#     )
#     return result.output
