import os
from dotenv import load_dotenv
from agents import AsyncOpenAI, OpenAIChatCompletionsModel
from agents.run import RunConfig


# Load the environment variables from the .env file
load_dotenv()

# Assuming GEMINI_API_KEY is for Google's Gemini through OpenAI-compatible API
gemini_api_key = os.getenv("GEMINI_API_KEY")

# Check if the API key is present; if not, raise an error
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")

#Reference: https://ai.google.dev/gemini-api/docs/openai
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash", # Or 'gemini-1.5-pro' for more robust reasoning if needed
    openai_client=external_client
)

gemini_config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True # Set to False if you want to see detailed traces
)



