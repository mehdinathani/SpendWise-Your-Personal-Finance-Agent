
# import sys
# import os
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agents import Agent, function_tool, Runner, RunContextWrapper
from tools.tools import ExpenseLookupTool
from models.model import UserQuery, SpendingSummary
from llm7config import config

# Tool decorated for LLM tool use (even though it's hardcoded/mock for now)
@function_tool
def summarize_budget(summary: SpendingSummary) -> str:
    """Summarizes user's budget performance and offers advice."""
    overspent = []
    for category, spent in summary.actuals.items():
        if spent > summary.budgets[category]:
            overspent.append(category)
    
    if not overspent:
        return "You're within budget in all categories! Great job 🟢💰"
    
    return f"You overspent in: {', '.join(overspent)}. Consider reducing spending in those areas next month. 🔍"

# Define the agent with tool
BudgetAdvisor = Agent(
    config=config,
    tools=[summarize_budget],
    instructions="""You are a Gen-Z friendly financial coach. Be helpful, concise, and informal.
                    You are given user spending data. Provide smart and empathetic advice."""
)

# Agent runner
runner = Runner(BudgetAdvisor)

# Function to route the query to the agent

def route_query(user_input: UserQuery) -> str:
    # Run the agent with the summary as tool input
    result = runner.run(
        BudgetAdvisor,
        input=user_input.query,
        tools=[summarize_budget]
        
    )
    return result.output
