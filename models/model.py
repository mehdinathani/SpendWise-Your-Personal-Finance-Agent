# models/model.py

from dataclasses import dataclass
from pydantic import BaseModel, Field
from typing import Dict

@dataclass
class BudgetContext:
    budgets: Dict[str, float]
    actuals: Dict[str, float]

# class UserQuery(BaseModel):
#     """
#     Input passed to the agent with query + budget context.
#     """
#     name: str = Field(..., example="Mehdi")
#     query: str = Field(..., example="Did I exceed my food budget?")
#     context: SpendingSummary
