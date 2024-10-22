import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_current_weather(location, unit="celsius"):
    """
    이 함수는 실제 날씨 정보를 반환합니다.
    실제 구현에서는 외부 API를 호출해야 합니다.
    """
    # 예시 데이터. 실제로는 API를 통해 이 정보를 가져와야 합니다.
    weather_data = {
        "location": location,
        "temperature": 22,
        "unit": unit,
        "condition": "맑음"
    }
    return json.dumps(weather_data)

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "주어진 위치의 현재 날씨 정보를 가져옵니다.",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "도시 이름, 예: 서울, 부산",
                    },
                    "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                },
                "required": ["location"],
            },
        }
    }
]

messages = [
    {"role": "system", "content": "당신은 날씨 정보를 제공하는 도우미입니다. get_current_weather 함수를 사용하여 날씨 정보를 얻을 수 있습니다."},
    {"role": "user", "content": "보스턴의 오늘 날씨는 어떤가요?"}
]

try:
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )

    if completion.choices[0].message.tool_calls:
        tool_call = completion.choices[0].message.tool_calls[0]
        function_name = tool_call.function.name
        function_args = json.loads(tool_call.function.arguments)
        
        if function_name == "get_current_weather":
            weather_result = get_current_weather(**function_args)
            messages.append({"role": "function", "name": function_name, "content": weather_result})
            
            final_response = client.chat.completions.create(
                model="gpt-4-0125-preview",
                messages=messages
            )
            
            print(final_response.choices[0].message.content)
    else:
        print("AI가 날씨 함수를 호출하지 않았습니다. 응답:", completion.choices[0].message.content)
except Exception as e:
    print(f"오류 발생: {str(e)}")
