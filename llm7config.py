import os
from dotenv import load_dotenv
from agents import AsyncOpenAI, OpenAIChatCompletionsModel, Runner, Agent
from agents.run import RunConfig
from openai.types.responses import ResponseTextDeltaEvent

import asyncio

load_dotenv()

llm7_api_key = os.getenv("LLM7_API_KEY", "unused")

external_client = AsyncOpenAI(
    api_key=llm7_api_key,
        base_url="https://api.llm7.io/v1",  # ✅ Critical to override default OpenAI URL
        )

model = OpenAIChatCompletionsModel(
    model="gpt-4o-mini-2024-07-18",  # You can change model ID from llm7.io
    openai_client=external_client
    )


config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
    )