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


def instructions(context_variables):
    xml_string = ""
    for key, value in context_variables.items():
        xml_string += f"<{key}>{value}</{key}>"
    return f"""
    You are a helpful agent.
    Introduce yourself with referring to following personal information.
    (You may skip if you don't have any personal information.)
    
    # Here is your personal information: \n{xml_string}

    """

agent = Agent(
    name="Agent",
    instructions=instructions,
)

# create a context variable
context_variables = {"name": "JAI", "job": "AI Engineer", "company": "abc"}

response = client.run(
    messages=[{"role": "user", "content": "안녕하세요."}],
    agent=agent,
    context_variables=context_variables
)
print(response.messages[-1]["content"])
