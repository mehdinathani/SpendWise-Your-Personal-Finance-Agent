# main.py

import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from agents.agents import run_multi_agent_advice

app = FastAPI()

# ---- Request/Response Models ---- #
class BudgetRequest(BaseModel):
    user_query: str
    budgets: dict  # example: {"food": 5000, "entertainment": 2000}

class AdviceResponse(BaseModel):
    response: str


@app.post("/get-advice", response_model=AdviceResponse)
def get_advice(request: BudgetRequest):
    response_text = run_multi_agent_advice(
        user_query=request.user_query,
        budgets=request.budgets
    )
    return {"response": response_text}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)


