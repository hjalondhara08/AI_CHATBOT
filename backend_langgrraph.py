from langgraph.graph import StateGraph,START,END
from typing import TypedDict,Annotated
from langchain_core.messages import HumanMessage,BaseMessage
from langgraph.checkpoint.memory import InMemorySaver
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq


 

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

checkpointer = InMemorySaver()
thred_id = 1

def chat_node(state: ChatState):

    # take user query from state
    messages = state['messages']

    # send to llm
    response = llm.invoke(messages)

    # response store state
    return {'messages': [response]}



graph = StateGraph(ChatState)

# add nodes
graph.add_node('chat_node', chat_node)

graph.add_edge(START, 'chat_node')
graph.add_edge('chat_node', END)

chatbot = graph.compile(checkpointer=checkpointer)

initial_state = {
    'messages': [HumanMessage(content='What is the capital of USA')],
    'config': {"configurable": {"thread_id": "user-1"}}
}

CONFIG = {"configurable": {"thread_id": "user-1"}}


result = chatbot.invoke( 
              {
             'messages': [HumanMessage(content='What is the capital of USA')],
              },
              config=CONFIG
            )

print(chatbot.get_state(config=CONFIG).values['messages'])
# print("Messages:", result['messages'])

# for message_chunk,metadata in chatbot.stream(
#   { 'messages':[HumanMessage(content="give me 70 line on ipl")]},
#   config={"configurable": {"thread_id": "1"}},
#   stream_mode="messages"
# ):
#    if message_chunk.content :
#       print(message_chunk.content, end=" ", flush=True)