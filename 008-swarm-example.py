from openai import OpenAI
from pydantic import BaseModel
from typing import Optional
import json
import inspect

client = OpenAI()

class Agent(BaseModel):
    name: str = "Agent"
    model: str = "gpt-4o-mini"
    instructions: str = "당신은 도움이 되는 에이전트입니다"
    tools: list = []

class Response(BaseModel):
    agent: Optional[Agent]
    messages: list

def function_to_schema(func):
    type_map = {
        str: "string", int: "integer", float: "number", bool: "boolean",
        list: "array", dict: "object", type(None): "null",
    }
    
    signature = inspect.signature(func)
    parameters = {}
    for param in signature.parameters.values():
        param_type = type_map.get(param.annotation, "string")
        parameters[param.name] = {"type": param_type}
    
    required = [param.name for param in signature.parameters.values() if param.default == inspect._empty]
    
    return {
        "type": "function",
        "function": {
            "name": func.__name__,
            "description": (func.__doc__ or "").strip(),
            "parameters": {
                "type": "object",
                "properties": parameters,
                "required": required,
            },
        },
    }

def execute_tool_call(tool_call, tools, agent_name):
    name = tool_call.function.name
    args = json.loads(tool_call.function.arguments)
    
    print(f"{agent_name}: {name}({args})")
    
    return tools[name](**args)

def run_full_turn(agent, messages):
    current_agent = agent
    num_init_messages = len(messages)
    messages = messages.copy()

    while True:
        tool_schemas = [function_to_schema(tool) for tool in current_agent.tools]
        tools = {tool.__name__: tool for tool in current_agent.tools}

        response = client.chat.completions.create(
            model=agent.model,
            messages=[{"role": "system", "content": current_agent.instructions}] + messages,
            tools=tool_schemas or None,
        )
        message = response.choices[0].message
        messages.append(message)

        if message.content:
            print(f"{current_agent.name}: {message.content}")

        if not message.tool_calls:
            break

        for tool_call in message.tool_calls:
            result = execute_tool_call(tool_call, tools, current_agent.name)

            if isinstance(result, Agent):
                current_agent = result
                result = f"{current_agent.name}로 전환되었습니다. 즉시 페르소나를 채택하세요."

            result_message = {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result,
            }
            messages.append(result_message)

    return Response(agent=current_agent, messages=messages[num_init_messages:])

def escalate_to_human(summary):
    print("인간 상담원에게 에스컬레이션 중...")
    print(f"\n=== 에스컬레이션 보고서 ===\n요약: {summary}\n=========================\n")
    exit()

def transfer_to_sales_agent():
    return sales_agent

def transfer_to_issues_and_repairs():
    return issues_and_repairs_agent

def transfer_back_to_triage():
    return triage_agent

def execute_order(product, price: int):
    print(f"\n=== 주문 요약 ===\n상품: {product}\n가격: ${price}\n=================\n")
    confirm = input("주문을 확인하시겠습니까? (y/n): ").strip().lower()
    if confirm == "y":
        print("주문이 성공적으로 실행되었습니다!")
        return "성공"
    else:
        print("주문이 취소되었습니다!")
        return "사용자가 주문을 취소했습니다."

def look_up_item(search_query):
    item_id = "item_132612938"
    print(f"아이템을 찾았습니다: {item_id}")
    return item_id

def execute_refund(item_id, reason="이유 제공되지 않음"):
    print(f"\n=== 환불 요약 ===\n아이템 ID: {item_id}\n이유: {reason}\n=================\n")
    print("환불이 성공적으로 실행되었습니다!")
    return "성공"

triage_agent = Agent(
    name="분류 에이전트",
    instructions="당신은 ACME Inc.의 고객 서비스 봇입니다. 자기소개를 하세요. 항상 매우 간단하게 대답하세요. 고객을 적절한 부서로 안내하기 위해 정보를 수집하세요. 하지만 질문을 자연스럽고 미묘하게 하세요.",
    tools=[transfer_to_sales_agent, transfer_to_issues_and_repairs, escalate_to_human],
)

sales_agent = Agent(
    name="판매 에이전트",
    instructions="당신은 ACME Inc.의 판매 에이전트입니다. 항상 한 문장 이하로 대답하세요. 다음 루틴을 따르세요: 1. 로드러너를 잡는 것과 관련된 삶의 문제에 대해 물어보세요. 2. ACME의 미친 가상 제품 중 하나가 도움이 될 수 있다고 가볍게 언급하세요. 가격은 언급하지 마세요. 3. 사용자가 동의하면 터무니없는 가격을 제시하세요. 4. 모든 것이 끝나고 사용자가 동의하면 미친 단서를 알려주고 주문을 실행하세요.",
    tools=[execute_order, transfer_back_to_triage],
)

issues_and_repairs_agent = Agent(
    name="문제 및 수리 에이전트",
    instructions="당신은 ACME Inc.의 고객 지원 에이전트입니다. 항상 한 문장 이하로 대답하세요. 다음 루틴을 따르세요: 1. 먼저 탐색적인 질문을 하고 사용자의 문제를 더 깊이 이해하세요. 사용자가 이미 이유를 제공한 경우는 제외합니다. 2. 해결책을 제안하세요 (만들어내세요). 3. 만족하지 않는 경우에만 환불을 제안하세요. 4. 수락되면 ID를 검색한 다음 환불을 실행하세요.",
    tools=[execute_refund, look_up_item, transfer_back_to_triage],
)

def main():
    agent = triage_agent
    messages = []

    print("ACME Inc. 고객 서비스에 오신 것을 환영합니다!")
    print("무엇을 도와드릴까요? (종료하려면 'quit'를 입력하세요)")
    print("챗봇: 안녕하세요! ACME Inc.의 고객 서비스입니다. 어떤 도움이 필요하신가요?")

    while True:
        user_input = input("사용자: ")
        if user_input.lower() == 'quit':
            print("채팅을 종료합니다. 감사합니다!")
            break

        messages.append({"role": "user", "content": user_input})

        response = run_full_turn(agent, messages)
        agent = response.agent
        messages.extend(response.messages)

if __name__ == "__main__":
    main()
