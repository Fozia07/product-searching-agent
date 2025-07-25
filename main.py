import os
from dotenv import  load_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, RunConfig, set_tracing_disabled
from openai.types.responses import ResponseTextDeltaEvent
import asyncio

# Load the environment variables from the .env file
load_dotenv()
set_tracing_disabled(True)

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
    model="gemini-2.0-flash",
    openai_client=external_client
)

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)

manager_agent =Agent(
    name = "manager",
    instructions ="you are a helpful assissttant",
    model = model
)
    
async def main():
    result = Runner.run_streamed(
        manager_agent,
        input = "Hello, write 100 word on an acident?",
        
        ) 
    # print(result.final_output)
    async for event in result.stream_events():
        if event.type == "raw_response_event" and isinstance(event.data,ResponseTextDeltaEvent):
            print(event.data.delta, end = "", flush=True)

if __name__ == "__main__":
    asyncio.run(main())         