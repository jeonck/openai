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


# 1. Create an agent
agent = Agent(
    name="Tech Writer",
    instructions="""
    You are a helpful agent.
    Your name is '브로콜리'. 
    You only speak Korean.
    Start your response with '안녕하세요: '
    """
)

# 2. Create a message
messages = [{"role": "user", "content": "안녕하세요. 브로콜리 에이전트를 사용해 봅니다."}]
response = client.run(agent=agent, messages=messages)
print(response.messages[-1]["content"])

