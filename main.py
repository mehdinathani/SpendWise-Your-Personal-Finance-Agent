# main.py

import asyncio
from agents import Runner
from models.model import BudgetContext
from my_agents.agents import BudgetAdvisor  # your actual Agent[BudgetContext]
# from llm7config import llm7_config
from geminiConfig import gemini_config

async def main():
    context = BudgetContext(
        budgets={"Food": 5000},
        actuals={"Food": 5500}
    )

    result = await Runner.run(
        starting_agent=BudgetAdvisor,
        input="Please use the analyze_spending tool to check if I am over or under my budget based on the given context.",
        context=context,
        run_config=gemini_config
    )

    print(result.final_output)
    print("Last agent used:", result.last_agent.name) # Print agent name for clarity
    print("Tools available:", BudgetAdvisor.tools)

if __name__ == "__main__":
    asyncio.run(main())
