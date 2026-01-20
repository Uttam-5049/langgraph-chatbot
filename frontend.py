import streamlit as st
from backend import agent, load_thread
from langchain_core.messages import HumanMessage
import uuid

def random_id():
    thread_id = uuid.uuid4()
    return thread_id

def reset_chat():
    thread_id = random_id()
    st.session_state['thread_id'] = thread_id
    add_thread(thread_id)
    st.session_state['messages'] = []

def add_thread(thread_id):
    if thread_id not in st.session_state['chat_thread_ids']:
        st.session_state['chat_thread_ids'].append(thread_id)

def load_conversation(thread_id):
    
    state = agent.get_state(config={'configurable': {'thread_id': thread_id}})
    return state.values.get('messages', [])

if 'messages' not in st.session_state:
    st.session_state['messages'] = []

if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = random_id()

if 'chat_thread_ids' not in st.session_state:
    st.session_state['chat_thread_ids'] = load_thread()

add_thread(st.session_state['thread_id'])

st.title("LangGraph ChatBot")

st.sidebar.title('Configuration')

if st.sidebar.button('new chat'):
    reset_chat()

st.sidebar.header('my conversations')

for thread_id in st.session_state['chat_thread_ids']:
    if st.sidebar.button(str(thread_id)):
        st.session_state['thread_id'] = thread_id
        CONFIG = {'configurable': {'thread_id': st.session_state['thread_id']}}
        messages = load_conversation(thread_id)
        
        temp_msg = []

        for message in messages:
            if isinstance(message, HumanMessage):
                role='user'
            else:
                role='assistant'

            temp_msg.append({'role':role, 'content': message.content})
        st.session_state['messages'] = temp_msg

for message in st.session_state['messages']:
    with st.chat_message(message['role']):
        st.write(message['content'])                    

user_input = st.chat_input("Type your message here...")

if user_input:

    st.session_state['messages'].append({'role': 'user', 'content': user_input})
    with st.chat_message('user'):
        st.write(user_input)

    CONFIG = {'configurable': {'thread_id': st.session_state['thread_id']}}

    with st.chat_message('assistant'):

        ai_message = st.write_stream(
            message_chunk.content for message_chunk, metadata in agent.stream(
                {'messages': [HumanMessage(content=user_input)]},
                config= CONFIG,
                stream_mode= 'messages'
            )
        )

    st.session_state['messages'].append({'role': 'assistant', 'content': ai_message})
