import streamlit as st
from utils import add_css, add_top_right_info, sidebar, set_background
import datetime
from openai import AzureOpenAI
import sys
import os
sys.path.append("backend")
from fastapicall import call_fastapi
import requests
from dotenv import load_dotenv
load_dotenv()

st.session_state['user_avatar'] = 'data/user.png'
st.session_state['assistant_avatar'] = 'data/system.png'
st.set_page_config(page_title='Chatbot', page_icon='data/page.png')
####################################################################
if 'is_input_disabled' not in st.session_state:
    st.session_state.is_input_disabled = False
###################### STREAMLIT INTERFACE ######################
def main_interface():
    st.title('Streamlit Chatbot')
    st.markdown(
        """
        <p style="font-size: 24px; margin: 0;">
            Welcome to the <span style="color: blue; font-weight: bold;"> Streamlit Chatbot </span> interface
        </p>
        """,
        unsafe_allow_html=True,
    )

    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    for entry in st.session_state.chat_history:
        if entry['role'] == 'user':
            with st.chat_message('user', avatar=st.session_state['user_avatar']):
                st.markdown(entry['content'])
                st.caption(f"{entry['timestamp']}")
        elif entry['role'] == 'assistant':
            with st.chat_message('assistant', avatar = st.session_state['assistant_avatar']):
                st.markdown(entry['content'])
                st.caption(f"{entry['timestamp']}") 
    user_input = st.chat_input("Type your message here...", disabled=st.session_state.is_input_disabled)

    if (user_input):
        st.session_state.is_input_disabled = True
        question_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.session_state['user_input'] = user_input
        st.session_state['question_timestamp'] = question_timestamp
        st.session_state.chat_history.append({"role": "user", "content": user_input, 'timestamp': question_timestamp})
        st.rerun()

###################### USER MESSAGE ######################
def user_message(user_input):
    if 'user_input' in st.session_state:

        messages = st.session_state.chat_history
        question_timestamp = st.session_state.question_timestamp
        try:
            with st.spinner('loading...'):
                answer_timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                data = call_fastapi(
                    messages=messages,
                    user_id=st.session_state.get("email"),
                    conversation_id=st.session_state.get("conversation_id"),
                )
                st.session_state["conversation_id"] = data.get("conversation_id", st.session_state.get("conversation_id"))
                response = data["answer"]
                
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": response,
                    "timestamp": answer_timestamp,
                    "metadata": data.get("metadata", {})
                })

                del st.session_state['user_input']
                st.session_state.is_input_disabled = False
                st.rerun()

        except Exception:
            error_message = (
                "An error occured"
            )
            with st.chat_message('assistant', avatar = st.session_state['assistant_avatar']):
                st.markdown(error_message)
            st.session_state.chat_history.append({'role': 'assistant', 'content': error_message})
            del st.session_state['user_input']
            st.session_state.is_input_disabled = False
            st.rerun()

def process_response(response):
    response = response.replace('\n', ' ')
    del st.session_state['user_input']
    st.session_state.is_input_disabled = False
    st.rerun()


def main():
    if "chat_history" not in st.session_state or not st.session_state.chat_history:
        st.session_state.chat_history = []
    main_interface()
    if 'user_input' in st.session_state:
        user_message(st.session_state['user_input'])


if __name__ == '__main__':
    if "email_entered" not in st.session_state:
        st.session_state["email_entered"] = False
    if not st.session_state.email_entered:
        email = st.text_input("Username:")
        if email:
            st.session_state.email = email
            st.session_state.email_entered = True
            st.rerun()
    else:
        email = st.session_state.email
        add_css()
        set_background('data/sea_image.png')
        add_top_right_info(email)
        # sidebar()
        main()