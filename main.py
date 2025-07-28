# main.py

import asyncio
from agents import Runner
from models.model import BudgetContext
from my_agents.agents import BudgetAdvisor  # your actual Agent[BudgetContext]
from llm7config import config

async def main():
    context = BudgetContext(
        budgets={"Food": 5000},
        actuals={"Food": 5500}
    )

    result = await Runner.run(
        starting_agent=BudgetAdvisor,
        input="how much budget i have for food, check my budget from context",
        context=context,
        run_config=config
    )

    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
