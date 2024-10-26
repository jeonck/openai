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
enlight_agent = Agent(
    name="Enlight Agent",
    instructions=""" 
    You only speak English.
    """
)

korean_agent = Agent(
    name="Korean Agent",
    instructions=""" 
    You only speak Korean.
    """
)

# 2. Create a function: 한국어 에이전트를 반환 
def transfer_to_korean_agent():
    """Transfer Koeran speaking users immediately."""
    return korean_agent

# 3. Add the function to the agent: 한국어 에이전트로 핸드오프
enlight_agent.functions.append(transfer_to_korean_agent)

messages = [{"role": "user", "content": "안녕하세요."}]
response = client.run(agent=enlight_agent, messages=messages)
print(response.messages[-1]["content"])
