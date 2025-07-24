# models/model.py

from pydantic import BaseModel, Field
from typing import Dict

class SpendingSummary(BaseModel):
    """
    Output from the ExpenseLookupTool.
    Used as context for the agent.
    """
    budgets: Dict[str, float] = Field(..., example={"Food": 5000})
    actuals: Dict[str, float] = Field(..., example={"Food": 6300})

class UserQuery(BaseModel):
    """
    Input passed to the agent with query + budget context.
    """
    name: str = Field(..., example="Mehdi")
    query: str = Field(..., example="Did I exceed my food budget?")
    context: SpendingSummary
