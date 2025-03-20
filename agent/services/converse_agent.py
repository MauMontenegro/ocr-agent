import os
from dotenv import load_dotenv
import json
from langchain_aws import ChatBedrockConverse
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode,tools_condition
from langgraph.graph import START,StateGraph
from langchain_core.messages import SystemMessage,HumanMessage


#-------------------------------------------
# Define State
from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages

class ConverseAgentState(TypedDict):
    messages : Annotated[list,add_messages]
#--------------------------------------------

load_dotenv()

# Parámetros del modelo
MODEL_ID= os.getenv("MODEL_ID_SCHEMA")

# Load Model
llm = ChatBedrockConverse(model_id=MODEL_ID)

# Define Nodes
def Chat(state:ConverseAgentState):
    return {"messages":state["messages"]}

# Define LangGraph logic Node
def process_query(state:ConverseAgentState):
    """Process a user question based on extracted OCR data.""" 
    # Generate response using LLM    
    response = llm.invoke(state["messages"])    
    return {"messages": response}

async def converse_agent_streamer(query: str):
    """Stream responses from the conversation agent"""
    graph = (StateGraph(ConverseAgentState)
             .add_node("query", process_query)
             .set_entry_point("query")
             .compile())
    
    message = [
        SystemMessage(content=(
        "You are a conversational agent."
        "Your goal is to answer user questions about a text extracted by an OCR service"          
    )),
        HumanMessage(content=query)]
    
    initial_state = {
        "messages": message,
    }    
    
    for chunk, metadata in graph.stream(initial_state, stream_mode="messages"):        
        if chunk.content and isinstance(chunk.content, list) and len(chunk.content) > 0:
            if 'text' in chunk.content[0]:
                
                yield chunk.content[0]['text']