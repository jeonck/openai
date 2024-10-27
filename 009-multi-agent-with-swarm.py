import os
import json
import inspect
from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from typing import Optional, Union
import streamlit as st
from tavily import TavilyClient
from langchain_community.tools import TavilySearchResults
from swarm import Swarm, Agent
import random


# .env 파일에서 환경 변수 로드
load_dotenv()

# OpenAI API 키 설정
# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Tavily API 키 설정
tavily_client = TavilyClient(api_key=os.getenv("TVLY_API_KEY"))

# Tool정의
# def search_perplexity(query: str) -> str:
#     """2024연도의 최신 정보를 웹 검색하는 기능"""
#     context = tavily_client.get_search_context(query=query)
#     return context

def search_on_web(query: str):
    """웹(구글, 네이버 등)에서 검색하고 결과를 반환합니다."""
    context = tavily_client.get_search_context(query=query)
    return context


def database_search_cat(query: str) -> str:
    """쿠키의 정보가 저장된 데이터베이스에서 검색하는 함수"""
    responses = [
      "쿠키는 최근 필라테스를 시작했습니다. 하지만 매번 스트레칭만 하다가 잠들어버립니다.",
      "쿠키는 몰래 '세계 정복 계획'을 세우고 있습니다. 첫 단계는 모든 냉장고를 점령하는 것이라고 합니다.",
      "쿠키는 최근 거울 속 자신과 싸움을 벌이고 있습니다. 현재 전적은 100승 0패 5무입니다.",
      "쿠키는 '고양이 말 번역기'를 개발 중입니다. 그런데 모든 번역 결과가 '츄르 내놔'로만 나오는 문제가 있네요.",
      "쿠키는 '츄르 맛 아이스크림' 상품 출시를 제안했습니다. 반려동물 카페계의 혁신이 될 것 같습니다.",
      "쿠키는 매일 밤 '그림자 놀이'를 연습합니다. 꼬리로 그리는 '한강의 밤'이 특기입니다."
    ]
    return random.choice(responses)


def database_search_dog(query: str) -> str:
    """해피의 정보가 저장된 데이터베이스에서 검색하는 함수"""
    responses = [
      "해피는 오늘도 꼬리를 신나게 흔들고 있습니다. 너무 세게 흔들어서 이제 선풍기급이 되었답니다.",
      "해피는 요즘 '사람 말' 배우기에 집중하고 있습니다. 하지만 아직 '멍멍'과 '끼잉'만 할 줄 압니다.",
      "해피는 몰래 고양이 간식을 탐내고 있습니다. 고양이 인형 탈을 쓰고 몰래 훔쳐 먹으려다 들켰다고 하네요.",
      "해피는 '전국 강아지 달리기 대회' 출전을 준비 중입니다. 현재 연습 기록은 100m 3초... 방향은 엉뚱한 곳으로.",
      "해피는 요즘 자기 그림자랑 술래잡기에 푹 빠졌습니다. 아직까지 한 번도 이기지 못했다고 합니다.",
      "해피는 '강아지용 AI 장난감'을 테스트 중입니다. 주요 기능은 '자동 간식 배출'과 '산책 시간 알림'입니다."
    ]
    return random.choice(responses)


# Agent의 정의
def transfer_to_router_agent():
    return router_agent

def transfer_to_web_search_agent():
    return Agent(
        name="Web Search Agent",
        instructions="당신은 Web Search Agent입니다. 최신 정보를 검색하여 답변을 생성합니다. 문장 끝에는 '뿅뿅'을 붙입니다",
        functions=[search_on_web, transfer_to_router_agent],
    )

def transfer_to_cookie_search_agent():
    return Agent(
        name="Database Search Agent",
        instructions="당신은 Database Search Agent입니다. 쿠키에 관한 정보가 저장된 데이터베이스에서 검색하여 답변을 생성합니다. 문장 끝에는 '냥냥'을 붙입니다",
        functions=[database_search_cat, transfer_to_router_agent],
    )


def transfer_to_happy_search_agent():
    return Agent(
        name="Database Search Agent",
        instructions="당신은 Database Search Agent입니다. 해피에 관한 정보가 저장된 데이터베이스에서 검색하여 답변을 생성합니다. 문장 끝에는 '멍멍'을 붙입니다",
        functions=[database_search_dog, transfer_to_router_agent],
    )

router_agent = Agent(
    name="Router Agent",
    instructions="""당신은 Router Agent입니다. 사용자의 질문에 대해 적절한 에이전트로 전달합니다.
    웹 검색이 필요한 경우는 transfer_to_web_search_agent를 호출하세요.
    쿠키에 관한 정보를 묻는 경우는 transfer_to_cookie_search_agent를 호출하세요.
    해피에 관한 정보를 묻는 경우는 transfer_to_happy_search_agent를 호출하세요.
    그 외의 경우에는 당신이 직접 답변하세요. 필요한 정보가 있다면 사용자에게 질문하세요.
    """,
    functions=[
        transfer_to_web_search_agent,
        transfer_to_cookie_search_agent,
        transfer_to_happy_search_agent,
    ],
)

def invoke_router_agent(user_input: str):
    messages = [{"role": "user", "content": user_input}]
    response = client.run(
        agent=router_agent,
        messages=messages,
        debug=True,
    )
    print(response.messages[-1]["content"])

def process_and_print_streaming_response(response):
    content = ""
    last_sender = ""

    for chunk in response:
        if "sender" in chunk:
            last_sender = chunk["sender"]

        if "content" in chunk and chunk["content"] is not None:
            if not content and last_sender:
                print(f"\033[94m{last_sender}:\033[0m", end=" ", flush=True)
                last_sender = ""
            print(chunk["content"], end="", flush=True)
            content += chunk["content"]

        if "tool_calls" in chunk and chunk["tool_calls"] is not None:
            for tool_call in chunk["tool_calls"]:
                f = tool_call["function"]
                name = f["name"]
                if not name:
                    continue
                print(f"\033[94m{last_sender}: \033[95m{name}\033[0m()")

        if "delim" in chunk and chunk["delim"] == "end" and content:
            print()  # End of response message
            content = ""

        if "response" in chunk:
            return chunk["response"]

def pretty_print_messages(messages) -> None:
    for message in messages:
        if message["role"] != "assistant":
            continue

        # print agent name in blue
        print(f"\033[94m{message['sender']}\033[0m:", end=" ")

        # print response, if any
        if message["content"]:
            print(message["content"])

        # print tool calls in purple, if any
        tool_calls = message.get("tool_calls") or []
        if len(tool_calls) > 1:
            print()
        for tool_call in tool_calls:
            f = tool_call["function"]
            name, args = f["name"], f["arguments"]
            arg_str = json.dumps(json.loads(args)).replace(":", "=")
            print(f"\033[95m{name}\033[0m({arg_str[1:-1]})")

def run_demo_loop(
    starting_agent, context_variables=None, stream=False, debug=False
) -> None:
    client = Swarm()
    print("Starting Swarm CLI 🐝")

    messages = []
    agent = starting_agent

    while True:
        user_input = input("User: ")
        if user_input.lower() == "q":
            print("Exiting the loop. Goodbye!")
            break  # Exit the loop
        messages.append({"role": "user", "content": user_input})

        response = client.run(
            agent=agent,
            messages=messages,
            context_variables=context_variables or {},
            stream=stream,
            debug=debug,
        )

        if stream:
            response = process_and_print_streaming_response(response)
        else:
            pretty_print_messages(response.messages)

        messages.extend(response.messages)


run_demo_loop(router_agent, stream=True)


