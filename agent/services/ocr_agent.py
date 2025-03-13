"""
Build The OCR Agent Workflow
"""

import os
from dotenv import load_dotenv

from langchain_aws import ChatBedrockConverse
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode,tools_condition
from langgraph.graph import START,END,StateGraph

# State
from agent.utils.state import OCRAgentState
# Tools
from agent.utils.tools import general_schematizer
from agent.utils.schemas import(tank_schema,oxxo_schema)
from agent.utils.prompts import(tank_task_prompt,oxxo_task_prompt,tank_additional_prompt,oxxo_additional_prompt)

# Cargando Variables de Entorno
load_dotenv()

# Parámetros del modelo
MODEL_ID = os.getenv("MODEL_ID")

# Load Model
llm = ChatBedrockConverse(model_id=MODEL_ID)

@tool
def tank_schematizer(ocr_text:str)-> str:
    """Structure a text that defines the state of gasoline tanks.
    The tanks can have the following features: Volúmen, temperatura, etc.
    """
    response = general_schematizer(
        ocr_text=ocr_text,
        schema=tank_schema,
        task_description=tank_task_prompt,
        additional=tank_additional_prompt)
    
    if response:
        return "Done"
    
    return "Not Done"

@tool
def oxxo_schematizer(ocr_text:str)-> str:
    """Structure a text that defines an OXXO ticket for selled products.      
    """
    response = general_schematizer(
        ocr_text=ocr_text,
        schema=oxxo_schema,
        task_description=oxxo_task_prompt,
        additional=oxxo_additional_prompt)
    
    if response:
        return "Done"
    
    return "Not Done"

# Bind Tools to Agent
tools = [tank_schematizer,oxxo_schematizer]
llm_w_tools = llm.bind_tools(tools)

# Definition of nodes (operations on states)
def schematizer(state:OCRAgentState):
    print(state["messages"][-1])    
    if "Done" in state["messages"][-1].content:
        print("Task Ended Succesfully!")
        return state               
    response = llm_w_tools.invoke(state["messages"][-1].content)          
    return{"messages":[response]}

# Graph Builder
def graph_builder():
    workflow = StateGraph(OCRAgentState)

    workflow.add_node("schema",schematizer)
    tool_node = ToolNode(tools=tools)
    workflow.add_node("tools",tool_node)

    workflow.add_conditional_edges("schema",tools_condition)

    workflow.add_edge(START,"schema")
    workflow.add_edge("tools","schema")

    ocr_agent = workflow.compile()

    return ocr_agent