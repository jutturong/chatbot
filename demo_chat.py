import os
from openai import OpenAI
import streamlit as st
def read_data_from_file(file_path):
 with open(file_path, "r", encoding="utf-8") as file:
        return file.read()
st.title("ChatGPT-like clone")
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"
if "messages" not in st.session_state:
    st.session_state.messages = []
# System prompt
system_prompt = read_data_from_file("system_prompt.txt")
if system_prompt:
    st.session_state.messages.append({"role": "assistant", "content": system_prompt})
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
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
    # st.session_state.messages.append({"role": "assistant", "content": response})