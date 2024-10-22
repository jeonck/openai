import os
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.title("OpenAI GPT 스트리밍 채팅")

user_input = st.text_input("메시지를 입력하세요:", "Hello!")

if st.button("전송"):
    message_placeholder = st.empty()
    full_response = ""
    
    for chunk in client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_input}
        ],
        stream=True
    ):
        content = chunk.choices[0].delta.content
        if content is not None:
            full_response += content
            message_placeholder.markdown(full_response + "▌")
    
    message_placeholder.markdown(full_response)
