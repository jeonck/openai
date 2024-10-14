# https://platform.openai.com/docs/api-reference/chat/create

from openai import OpenAI
import os
os.environ["OPENAI_API_KEY"] = "sk-***"

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def run_gpt(model:str, messages:list, max_tokens:int=150, temperature:float=0.7):
  response = client.chat.completions.create(
    model=model,
    messages=messages,
    max_tokens=max_tokens,
    temperature=temperature,
)

return response


system_message = "너는 유능한 비서야"
user_message = f"""회의 녹취본을 제공할게. 이 내용을 바탕으로 회의록을 작성해줘. 단, 회의록 작성의 조건은 다음과 같아.
조건:
1. 녹취본을 보고 회의의 전반적인 핵심 주제를 1~2 문장으로 요약해줘. 이 때, bullet point 형식을 사용해줘.
2. 참석자 별로 발언 내용을 정리해줘. 발언 내용은 각 참석자가 말한 핵심 내용을 요약해주면 돼. 역시 1~2개의 bullet point로 요약해줘.
3. 참석자 별로 Action Item이 있다면 모든 Action Item을 bullet point로 정리해줘. Action Item은 누가, 언제까지, 무엇을 할지 명확하게 작성해줘. 만약 참석자에게 Action Item이 없다면 '없음'이라고 작성해줘.
—
회의 녹취본:
{transcript}
"""

messages = [
    {"role": "system", "content": system_message},
    {"role": "user", "content": user_message}
]

# 파라미터2: model
model = "gpt-4o"
# 파라미터3: max_tokens
max_tokens = 1500

response = run_gpt(model, messages, max_tokens,)
print(response.choices[0].message.content)
