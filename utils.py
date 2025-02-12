import os
import openai
import random
import streamlit as st
from datetime import datetime
from openai import OpenAIError

# decorator
def enable_chat_history(func):
    def execute(*args, **kwargs):
        # to clear chat history after switching chatbot
        current_page = func.__qualname__
        if "current_page" not in st.session_state:
            st.session_state["current_page"] = current_page
        if st.session_state["current_page"] != current_page:
            try:
                st.cache_resource.clear()
                del st.session_state["current_page"]
                del st.session_state["messages"]
            except KeyError:
                pass

        # to show chat history on ui
        if "messages" not in st.session_state:
            st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]
        for msg in st.session_state["messages"]:
            st.chat_message(msg["role"]).write(msg["content"])

        func(*args, **kwargs)
    return execute

def display_msg(msg, author):
    """Method to display message on the UI

    Args:
        msg (str): message to display
        author (str): author of the message -user/assistant
    """
    st.session_state.messages.append({"role": author, "content": msg})
    st.chat_message(author).write(msg)

def configure_openai():
    # 安全获取API密钥
    dashscope_api_key = os.getenv("DASHSCOPE_API_KEY")
    if not dashscope_api_key:
        st.error("Missing DashScope API key in secrets")
        st.stop()

    st.session_state['DASHSCOPE_API_KEY'] = dashscope_api_key
    os.environ['OPENAI_API_KEY'] = dashscope_api_key

    # 配置自定义API端点
    api_base = "https://dashscope.aliyuncs.com/compatible-mode/v1"

    try:
        client = openai.OpenAI(
            api_key=dashscope_api_key,
            base_url=api_base,
        )
        # 直接指定支持的模型列表
        model = "qwen-plus"
        return model
    except OpenAIError as e:
        st.error(f"OpenAI API Error: {e}. Please check your API key and try again.")
        st.stop()
    except Exception as e:
        st.error(f"Unexpected error: {str(e)}")
        st.stop()
