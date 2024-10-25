# https://platform.openai.com/docs/assistants/quickstart/step-1-create-an-assistant

import os
import time
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 1. Create an assistant
assistant = client.beta.assistants.create(
    name="Tech Writer",
    instructions="""
    당신은 블로그 글 작성에 10년 이상의 경험을 가진 전문가 입니다. 
    주제만 입력하면 서론, 본론, 결론을 나누어 잘 작성해 줍니다. 
    읽는 동안 이해가 쉽도록 비유를 들어 독자의 이해를 돕습니다. 
    중요한 개념에 대해서는 예시를 들어 구체화된 정보를 제시해 줍니다. 
    """,
    model="gpt-4o-mini",
)

print(assistant.id)

# 2. Create a thread
thread = client.beta.threads.create()

print(thread.id)

# 3. 사용자로부터 주제 입력 받기
topic = input("기술 블로그 주제를 입력해주세요: ")

# 4. 주제를 포함한 메시지를 스레드에 추가
client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content=f"다음 주제에 대한 기술 블로그 글을 작성해주세요: {topic}",
)

# 5. 어시스턴트 실행
run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=assistant.id,
    instructions=f"'{topic}'에 대한 기술 블로그 글을 작성해주세요. 서론, 본론, 결론 구조로 작성하고, 비유와 예시를 포함해주세요.",
)

print(run.id)

# 6. Get the run results
while True:
    run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
    if run.status == "completed":
        messages = client.beta.threads.messages.list(thread_id=thread.id)
        print("\n=== 기술 블로그 글 작성 완료 ===\n")
        for message in messages:
            if message.role == "assistant":
                print(message.content[0].text.value)
        break
    elif run.status == "failed":
        print("글 작성에 실패했습니다.")
        break
    else:
        print(f"글 작성 중... (상태: {run.status})")
        time.sleep(5)

# 7. Delete the thread
client.beta.threads.delete(thread.id)

