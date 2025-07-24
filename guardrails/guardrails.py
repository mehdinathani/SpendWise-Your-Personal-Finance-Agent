import re
from agents import input_guardrail, output_guardrail
from agents import RunContextWrapper, GuardrailFunctionOutput
from pydantic import BaseModel

# Define the context structure expected
class BudgetContext(BaseModel):
    budgets: dict[str, int]  # e.g., {"food": 5000, "travel": 10000}

@input_guardrail
async def budget_input_guardrail(
    ctx: RunContextWrapper[BudgetContext],
    agent,
    input: str | list
) -> GuardrailFunctionOutput:
    """
    Guardrail to stop input if user mentions spending above allowed budget.
    Looks for patterns like "I spent 7000 on food".
    """

    user_query = input if isinstance(input, str) else str(input)
    budgets = ctx.context.budgets if ctx.context and ctx.context.budgets else {}

    # Basic spending pattern extraction
    matches = re.findall(r"spent\s+(\d+)\s+on\s+(\w+)", user_query.lower())
    
    for amount_str, category in matches:
        amount = int(amount_str)
        budget_limit = budgets.get(category)
        if budget_limit is not None and amount > budget_limit:
            return GuardrailFunctionOutput(
                output_info={"exceeded": True, "category": category, "amount": amount},
                tripwire_triggered=True,
            )

    return GuardrailFunctionOutput(
        output_info={"exceeded": False},
        tripwire_triggered=False,
    )


@output_guardrail
def check_output_guardrail(advice: str) -> str | None:
    """
    Guardrail to detect vague or short advice from LLM.
    """
    word_count = len(advice.split())
    vague_keywords = ["maybe", "possibly", "can't say", "not sure"]

    if word_count < 10:
        return "Output Guardrail Triggered: Advice too short"

    if any(kw in advice.lower() for kw in vague_keywords):
        return "Output Guardrail Triggered: Advice too vague"

    return None
