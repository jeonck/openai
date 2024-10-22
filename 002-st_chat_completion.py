# https://platform.openai.com/docs/api-reference/chat/create

import streamlit as st
from openai import OpenAI

# 스트림릿 앱 설정
st.set_page_config(page_title="OpenAI Chat Completion")
st.title("OpenAI Chat Completion")

# API 키 입력 받기
api_key = st.text_input("OpenAI API 키를 입력하세요:", type="password")

# 사용자 입력 받기
user_input = st.text_input("메시지를 입력하세요:")

if st.button("전송") and api_key and user_input:
    try:
        # OpenAI 클라이언트 생성
        client = OpenAI(api_key=api_key)

        # Chat completion 요청
        completion = client.chat.completions.create(
            model="gpt-4o-mini",  
            messages=[
                {"role": "system", "content": "당신은 도움이 되는 어시스턴트입니다."},
                {"role": "user", "content": user_input}
            ]
        )

        # 응답 출력
        st.write("응답:", completion.choices[0].message.content)
    except Exception as e:
        st.error(f"오류가 발생했습니다: {str(e)}")
else:
    st.info("API 키와 메시지를 입력한 후 '전송' 버튼을 클릭하세요.")
