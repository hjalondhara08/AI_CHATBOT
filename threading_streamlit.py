
import streamlit as st
from backend_langgrraph import chatbot 
from database_langgraph import retrieve_all_threads
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import InMemorySaver
import uuid

from database_langgraph import retrieve_all_threads

config = {"configurable": {"thread_id": "1"}}
#****************************Utility Functions *****************************
def thread_id_generator():
    thread_id = uuid.uuid4()
    return thread_id

def reset_chat():
    thread_id = thread_id_generator()
    st.session_state['thread_id'] = thread_id
    add_thread(st.session_state['thread_id'])
    st.session_state['message_history'] = []

def add_thread(thread_id):
    if thread_id not in st.session_state['chat_thread']:
        st.session_state['chat_thread'].append(thread_id)

def load_conversation(thread_id):
    state = chatbot.get_state(config={'configurable': {'thread_id': thread_id}})
    # Check if messages key exists in state values, return empty list if not
    return state.values.get('messages', [])


#****************************SESSION STATE *****************************

if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []


if 'thread_id' not in st.session_state :
    st.session_state['thread_id'] = thread_id_generator()

if 'chat_thread' not in st.session_state:
    st.session_state['chat_thread'] = retrieve_all_threads()

add_thread(st.session_state['thread_id'])



#****************************SIDE BAR *****************************

st.sidebar.title("Chat History")
if st.sidebar.button('new chat'):
    reset_chat()


st.sidebar.header('my coversations')

for thread_id in st.session_state['chat_thread'][::-1 ]:
    if st.sidebar.button(str(thread_id)):
        st.session_state['thread_id'] = thread_id
        messages = load_conversation(thread_id)
       
        temp_messages = []

        for msg in messages:
            if isinstance(msg, HumanMessage):
                role='user'
            else:
                role='assistant'
            temp_messages.append({'role': role, 'content': msg.content})

        st.session_state['message_history'] = temp_messages
              


#****************************MAIN CODE*****************************

for message in st.session_state['message_history']:
    with st.chat_message(message["role"]):
        st.text(message["content"])

user_input = st.chat_input("Enter your message:")

if user_input:
    response = chatbot.invoke({'messages': [HumanMessage(content=user_input)]}, config=config)
    result = response['messages'][-1].content

    st.session_state['message_history'].append({'role':'user','content':user_input})
    with st.chat_message("user"):
        st.write(user_input)
    

    config = {"configurable": {"thread_id": st.session_state['thread_id']}}
    with st.chat_message("assistant"):

     ai_message =  st.write_stream(
      message_chunk.content for message_chunk,metadata in chatbot.stream(
      { 'messages':[HumanMessage(content=user_input)]},
      config=config,
      stream_mode="messages"
    )
    )
    st.session_state['message_history'].append({'role':'AI','content':ai_message})

