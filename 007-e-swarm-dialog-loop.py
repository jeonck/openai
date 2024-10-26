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

my_agent = Agent(
    name="My Agent",
    instructions="You are a helpful agent.",
)

def pretty_print_messages(messages):
    if len(messages) > 0:
        print(f"{messages[-1]['role']}: {messages[-1]['content']}")

messages = []
agent = my_agent

while True:
    user_input = input("You: ")
    if user_input.strip().lower() in ["exit", "quit", "bye", "goodbye", "q"]:
        break
    messages.append({"role": "user", "content": user_input})
    pretty_print_messages(messages)
    response = client.run(agent=agent, messages=messages)
    messages.append({"role": "assistant", "content": response.messages[-1]["content"]})
    agent = response.agent
    pretty_print_messages(messages)
