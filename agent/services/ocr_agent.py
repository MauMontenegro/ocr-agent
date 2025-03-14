"""
Build The OCR Agent Workflow
"""

import os
from dotenv import load_dotenv

from langchain_aws import ChatBedrockConverse
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode,tools_condition
from langgraph.graph import START,StateGraph
from langchain_core.messages import HumanMessage, SystemMessage

# State
from agent.utils.state import OCRAgentState
# Tools
from agent.utils.tools import general_schematizer
from agent.utils.schemas import(tank_schema,oxxo_schema)
from agent.utils.prompts import(tank_task_prompt,oxxo_task_prompt,tank_additional_prompt,oxxo_additional_prompt)

from agent.services.textract import textract_service

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Cargando Variables de Entorno
load_dotenv()

# Parámetros del modelo
MODEL_ID= os.getenv("MODEL_ID_SCHEMA")

# Load Model
llm = ChatBedrockConverse(model_id=MODEL_ID)

@tool
def tank_schematizer(ocr_text:str)-> str:
    """Structure a text that defines the state of gasoline tanks.
    The tanks can have the following features: Volúmen, temperatura, etc.
    """
    print("Usando Tool de Tanques.",flush=True)
    response = general_schematizer(
        ocr_text=ocr_text,
        schema=tank_schema,
        task_description=tank_task_prompt,
        additional=tank_additional_prompt,
        doc_type="tank")
    
    if response:
        return "Done"
    
    return "Not Done"

@tool
def oxxo_schematizer(ocr_text:str)-> str:
    """Structure a text that defines an OXXO ticket for selled products.      
    """
    print("Usando Tool de Oxxo.")
    response = general_schematizer(
        ocr_text=ocr_text,
        schema=oxxo_schema,
        task_description=oxxo_task_prompt,
        additional=oxxo_additional_prompt,
        doc_type="oxxo")
    
    print(response)
    if response:
        return "Done"
    
    return "Not Done"

# Bind Tools to Agent
llm_w_tools = llm.bind_tools([tank_schematizer,oxxo_schematizer])

# Definition of nodes (operations on states)
def schematizer(state:OCRAgentState):
    print(state["messages"][-1].content)   
    if "Done" in state["messages"][-1].content:        
        return state              
    response = llm_w_tools.invoke(state["messages"][-1].content)
    print(response)           
    return{"messages":[response]}

def ocr_step(state:OCRAgentState):
    extracted_text = textract_service(state["file"])   
    state["extracted_text"] = extracted_text
    return{
        "messages":[
            HumanMessage(
                content=f"This is the OCR text:{extracted_text}"
                )
            ]
        }

# Graph Builder
def graph_builder(image_bytes):
    workflow = StateGraph(OCRAgentState)

    workflow.add_node("schema",schematizer)
    workflow.add_node("ocr",ocr_step)    
    tool_node = ToolNode(tools=[tank_schematizer,oxxo_schematizer])
    workflow.add_node("tools",tool_node)
    workflow.add_conditional_edges("schema",tools_condition)

    workflow.add_edge(START,"ocr")
    workflow.add_edge("ocr","schema")    
    workflow.add_edge("tools","schema")
    
    ocr_agent = workflow.compile()

    message = [
        SystemMessage(content=(
        "You are an agent responsible for analyzing texts extracted via OCR and processing them based on their content."
        "Use the right tool based on the extracted text."    
    ))]

    initial_state={
        "messages":message,
        "file":image_bytes,  
    }

    ocr_agent.invoke(initial_state)

    return "Task Ended Succesfully"