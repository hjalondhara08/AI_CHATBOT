from langgraph.graph import StateGraph,START,END
from typing import TypedDict,Annotated
from langchain_core.messages import HumanMessage,BaseMessage
from langgraph.checkpoint.sqlite import SqliteSaver
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
import sqlite3


 

# Load environment variables
load_dotenv()

# Read API key from .env
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

llm = ChatGroq(
    api_key=os.getenv("GROQ_API_KEY"),
    model="openai/gpt-oss-120b",
)

# print(llm.invoke("hi"))


from langgraph.graph import message
from langgraph.graph.message import add_messages
from langgraph.graph.message import add_messages

class ChatState(TypedDict):
   messages : Annotated[list[BaseMessage],add_messages]



def chat_node(state: ChatState):

    # take user query from state
    messages = state['messages']

    # send to llm
    response = llm.invoke(messages)

    # response store state
    return {'messages': [response]}


conn = sqlite3.connect(database="chatbot.db",check_same_thread=False)
checkpointer = SqliteSaver(conn=conn)

graph = StateGraph(ChatState)

# add nodes
graph.add_node('chat_node', chat_node)

graph.add_edge(START, 'chat_node')
graph.add_edge('chat_node', END)

chatbot = graph.compile(checkpointer=checkpointer)

checkpointer.list(None)

def retrieve_all_threads():
    all_thread = set()
    for checkpoint in checkpointer.list(None):
        all_thread.add(checkpoint.config['configurable']['thread_id'])
    return list(all_thread)

all_threads = retrieve_all_threads()

print("All thread IDs:", all_threads)



# initial_state = {
#     'messages': [HumanMessage(content='What is the capital of USA')],
#     'config': {"configurable": {"thread_id": "user-1"}}
# }

# result = chatbot.invoke(initial_state, config={"configurable": {"thread_id": "user-1"}})
# print("Result:", result)
# print("Messages:", result['messages'])

# for message_chunk,metadata in chatbot.stream(
#   { 'messages':[HumanMessage(content="give me 70 line on ipl")]},
#   config={"configurable": {"thread_id": "1"}},
#   stream_mode="messages"
# ):
#    if message_chunk.content :
#       print(message_chunk.content, end=" ", flush=True)

response = chatbot.invoke(
      { 'messages':[HumanMessage(content="what is your model name")]},
         config={"configurable": {"thread_id": "4"}},
    )



print(response)





