import os
import asyncio

from pydantic_ai import Agent, RunContext
from pydantic_ai.models.google import GoogleModel
from pydantic_ai.providers.google import GoogleProvider
from pydantic import BaseModel
from dotenv import load_dotenv
from dataclasses import dataclass

load_dotenv()

@dataclass # used for agent context
class MyDeps:
    name: str

# structured output type shii
class OutputType(BaseModel):
    food: str
    name: str

# provider setup
provider = GoogleProvider(api_key=os.getenv('GEMINI_API_KEY'))
model = GoogleModel('gemini-2.5-flash-lite', provider=provider)
agent = Agent(model, deps_type=MyDeps, system_prompt="You MUST say 'Hi [insert user name]' at the start of your reply.")

# declare system prompt
@agent.system_prompt
def get_name(ctx: RunContext[MyDeps]) -> str:
    return (
        f"The user's name is {ctx.deps.name}. "
        f"CRITICAL: You MUST start your response with 'Hi {ctx.deps.name}'."
    )

# tool to get fav food
@agent.tool
def get_favourite_food(ctx: RunContext[MyDeps]) -> str:
    """
    Returns the user's favourite food.
    """
    name = ctx.deps.name
    print(f"Getting favourite food for {name}...")
    if name == "Mike":
        return "Pizza"
    elif name == "Parth":
        return "Sushi"
    else:
        return "I don't know your favourite food."

# actual run
async def main():
    deps = MyDeps("Mike")
    res = await agent.run("What is the user's fav food?", deps=deps, output_type=OutputType)
    print(res.output)


asyncio.run(main())