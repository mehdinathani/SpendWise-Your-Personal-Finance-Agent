from pydantic import BaseModel
from agents import (
    Agent,
    GuardrailFunctionOutput,
    input_guardrail,
    TResponseInputItem, 
    Runner,
    RunContextWrapper,
    output_guardrail,

)

from geminiConfig import gemini_config
from llm7config import llm7_config


class userMessageCheck(BaseModel):
    is_valid_input : bool
    reasoning : str

class agentMessageCheck(BaseModel):
    is_valid_output : bool
    reasoning : str
    output : str


guardrail_input_agent = Agent(
    name="Guardrail Check",
    instructions="check if the user input is relevent to there financial transaction or financial analyse from context, and max 2 sentences",
    output_type=userMessageCheck
)

guardrail_output_agent = Agent(
    name="Guardrail check for agent",
    instructions="Check agent output, if its too long, hallacunus, or generic like i m just an AI, contains sensitive information or failed to answer",
    output_type=agentMessageCheck
)

@input_guardrail
async def check_user_input_guardrail(
        ctx: RunContextWrapper[None], agent: Agent, input: str | list[TResponseInputItem]
) -> GuardrailFunctionOutput:
    result = await Runner.run(
        guardrail_input_agent,
        input=input,
        run_config=gemini_config,
        context=ctx.context
    )
    print("Guardrails output")
    print(result.final_output)
    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered = not result.final_output.is_valid_input ,
    )

@output_guardrail
async def check_agent_output_guardrail(
    ctx: RunContextWrapper[None], agent : Agent, input : str | list[TResponseInputItem]
) -> GuardrailFunctionOutput:
    result = await Runner.run(
        guardrail_output_agent,
        input = input,
        context=ctx.context,
        run_config=gemini_config
    )
    print("outputGuardrails output")
    print(result.final_output)
    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered = not result.final_output.is_valid_output ,
    )