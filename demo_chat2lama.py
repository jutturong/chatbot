import os
from openai import OpenAI
import streamlit as st
def read_data_from_file(file_path):
 with open(file_path, "r", encoding="utf-8") as file:
        return file.read()
st.title("ChatGPT-like clone")
AI_MODEL="llama3.2:latest"
client = OpenAI(
    base_url="http://178.128.80.149:11434/v1",
    api_key="xxxxx",
    )
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = AI_MODEL
if "messages" not in st.session_state:
    st.session_state.messages = []
# System prompt
system_prompt = """
Here is FAQ for my shop:
Q: ค่าส่งเท่าไร
A: ระบบมีการคำนวณค่าส่งให้อัตโนมัติ หลังจากที่ท่านเลือกสินค้าแล้ว ให้กดเข้าไปดูที่หน้าตะกร้าสินค้า ด้านล่างจะแสดงราคาของวิธีการส่งแบบต่าง ๆ ที่สามารถจัดส่งได้ ขึ้นกับน้ำหนักของสินค้าที่ท่านเลือกไว้ในตะกร้านะคะ
Q: มีขั้นต่ำในการสั่งสินค้าหรือไม่
A: ไม่มีค่ะ
Q: มีสั่งเยอะแค่ไหนแล้วส่งฟรีมั๊ย
A: ไม่มีเช่นกันค่ะ ค่าสินค้าเราไม่ได้แอบบวกค่าจัดส่ง ทำให้เรามีระบบคิดค่าจัดส่งแยก การจัดส่งสินค้ามีค่าจัดส่งค่ะ
"""
assistant_prompt = """
Instruction:
Super chatbot for question/answer for shop
Given FAQ for my shop, can you assist customer
Output format: ตอบเป็นภาษาไทยเสมอ
"""
st.session_state.messages.append({"role": "system", "content": system_prompt})
st.session_state.messages.append({"role": "assistant", "content": assistant_prompt})
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["role"] == "user":
            st.markdown(message["content"])
if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=AI_MODEL,
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
    # st.session_state.messages.append({"role": "assistant", "content": response})