# https://docs.tvly.ai/docs/getting-started
# https://github.com/teddylee777/swarm
import os
import time
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("TVLY_API_KEY"))

from swarm import Swarm, Agent

client = Swarm()


def get_weather(location: str) -> str:
    """Get the current weather in a given location."""
    return "{'temp': 20, 'unit': 'C'}"

agent = Agent(
    name="Weather Agent",
    instructions="You are a helpful agent that can only get the weather.",
    functions=[get_weather],
)

messages = [{"role": "user", "content": "서울의 날씨는 어때?"}]
response = client.run(agent=agent, messages=messages)
print(response.messages[-1]["content"])
