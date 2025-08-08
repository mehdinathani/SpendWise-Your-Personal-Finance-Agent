# tools/tools.py

import random
from typing import Dict

from agents import function_tool, RunContextWrapper
from pydantic import BaseModel, Field
from models.model import BudgetContext


class SpendingAnalysisInput(BaseModel):
    budgets: Dict[str, float] = Field(..., description="A dictionary of budget categories and amounts.")
    actuals: Dict[str, float] = Field(..., description="A dictionary of actual spending categories and amounts.")


class ExpenseLookupTool:
    """
    Mock expense retrieval tool.
    In real scenario, this would query a DB or data source.
    """
    def run(self, budgets: dict, actuals: dict = None) -> BudgetContext:
        # Simulate actuals if not passed
        if actuals is None:
            actuals = {
                k: random.randint(int(v * 0.6), int(v * 1.4))  # ±40% variation
                for k, v in budgets.items()
            }
        
        return BudgetContext(
            budgets=budgets,
            actuals=actuals
        )

@function_tool
async def analyze_spending(wrapper : RunContextWrapper[BudgetContext]) -> str:
    """Provide advice based on user's budget and actuals."""
    print("analyze_spending tool called with Pydantic model")
    ctx = wrapper.context

    food_budget = ctx.budgets.get("Food", 0)
    food_actual = ctx.actuals.get("Food", 0)

    if food_actual > food_budget:
        return f"You are overspending on Food! Budget: {food_budget}, Actual: {food_actual}"
    elif food_actual < food_budget:
        return f"Great job! You are under budget on Food. Budget: {food_budget}, Actual: {food_actual}"
    return "Your food spending is exactly on budget."
