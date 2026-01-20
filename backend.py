from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph.message import add_messages
from dotenv import load_dotenv
import sqlite3

load_dotenv()

class State(TypedDict):
    messages : Annotated[list[BaseMessage], add_messages]

model=ChatOpenAI(model_name="gpt-4", temperature=0)

def model_query(state: State):
    messages = state["messages"]
    response = model.invoke(messages)
    return {'messages' : [response]}


graph = StateGraph(State)

graph.add_node("model_query", model_query)
graph.add_edge(START, "model_query")
graph.add_edge("model_query", END)

conn = sqlite3.connect(database='chatbot.db', check_same_thread=False)
saver = SqliteSaver(conn=conn)

agent = graph.compile(checkpointer=saver)

CONFIG = {'configurable': {'thread_id': 241}}

response = agent.invoke({'messages': [HumanMessage(content="Hello, what is your name?")]}, config=CONFIG)

print(response)

def load_thread():
    all_threads = set()
    for thread_id in saver.list(None):
        all_threads.add(thread_id.config["configurable"]["thread_id"])
    
    return list(all_threads)