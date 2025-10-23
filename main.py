import asyncio
import os
from random import randint
from typing import Annotated

from agent_framework import ChatAgent
from agent_framework.openai import OpenAIChatClient
from openai import AsyncOpenAI


# Define tool(s) and add to 'ChatAgent'
def get_weather(
    location: Annotated[str, "The location to get the weather for."],
) -> str:
    """Get the weather for a given location."""
    conditions = ["sunny", "cloudy", "rainy", "stormy"]
    return f"The weather in {location} is {conditions[randint(0, 3)]} with a high of {randint(10, 30)}°C."


async def main() -> None:
    github_token = os.environ.get("GITHUB_TOKEN")
    if not github_token:
        print("Please set the GITHUB_TOKEN environment variable.")
        return

    openai_client = AsyncOpenAI(
        base_url="https://models.github.ai/inference",
        api_key=github_token,
    )
    chat_client = OpenAIChatClient(
        async_client=openai_client, model_id="openai/gpt-4o-mini"
    )
    agent = ChatAgent(
        chat_client=chat_client,
        name="HB_Tools",
        instructions="You are HB_Tools, a helpful AI agent that provides various tools and assistance.",
        tools=[get_weather],
    )

    # Example interaction
    result = await agent.run("What's the weather like in Seattle?")
    print(f"HB_Tools: {result.text}")


if __name__ == "__main__":
    asyncio.run(main())
