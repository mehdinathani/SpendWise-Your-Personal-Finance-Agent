# tools/tools.py

import random
from models.model import BudgetContext

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
