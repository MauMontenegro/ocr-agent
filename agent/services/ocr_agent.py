"""
Build The OCR Agent Workflow
"""

import os
from dotenv import load_dotenv

from langchain_aws import ChatBedrockConverse
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode,tools_condition
from langgraph.graph import START,StateGraph
from langchain_core.messages import SystemMessage,AIMessage,ToolMessage


from langgraph.types import Command

# State
from agent.utils.state import OCRAgentState
# Tools
from agent.utils.tools import general_schematizer
from agent.utils.prompts import(tank_task_prompt,oxxo_task_prompt)

from agent.services.textract import textract_service
from agent.utils.tools import classify

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
def tank_schematizer(ocr_text: str) -> str:
    """Structure a text that defines the state of gasoline tanks.
    The tanks can have the following features: Volúmen, temperatura, etc.
    """
    print("Usando Tool de Tanques.", flush=True)
    response,schema = general_schematizer(
        ocr_text=ocr_text,       
        task_description=tank_task_prompt,        
        doc_type="tank")    
    return Command(
        update={            
            "structured_text": schema,            
            "messages": [
                ToolMessage(
                    content=response, tool_call_id="1234",
                )
            ],
        }
    ) 

@tool
def oxxo_schematizer(ocr_text: str) -> str:
    """Structure a text that defines an OXXO ticket for selled products.      
    """
    print("Usando Tool de Oxxo.")
    response,schema = general_schematizer(
        ocr_text=ocr_text,       
        task_description=oxxo_task_prompt,        
        doc_type="oxxo")
    return Command(
        update={            
            "structured_text": schema,            
            "messages": [
                ToolMessage(
                    content=response, tool_call_id="1234",
                )
            ],
        }
    )   
    

tools=[tank_schematizer,oxxo_schematizer]

# Bind Tools to Agent
llm_w_tools = llm.bind_tools(tools)

tool_node = ToolNode(tools)

# Definition of nodes (operations on states)
def schematizer(state:OCRAgentState):      
    if isinstance(state["messages"][-1], ToolMessage) and "Done" in state["messages"][-1].content:
        return state
    ocr_text = state["extracted_text"]
    full_ocr_text = "\n".join(ocr_text)
    choosen_tool = state["tool_t_call"]    
    choosen_tool = choosen_tool.strip().strip('"\'')     
    message_w_tool_call=AIMessage(
                                    content="",
                                    tool_calls=[
                                        {
                                            "name": choosen_tool,
                                            "args": {"ocr_text": full_ocr_text},            
                                            "type": "tool_call",
                                            "id": "1234",
                                        }
                                    ],
                                )
    state["messages"].append(message_w_tool_call)
    response = tool_node.invoke({"messages": [message_w_tool_call]})    
    if "messages" in response and response["messages"]:
        tool_response = response["messages"][0]
        state["messages"].append(tool_response)    
    return {"messages":state["messages"]}
    

def classifier(state:OCRAgentState):
    print("Cassify") 
    doc_type = classify(state["extracted_text"][:500])
    tool_t_call = doc_type.content.strip().lower()
    print(f"Tool to call after classify:{tool_t_call}")
    return{"messages":state["messages"],"tool_t_call":tool_t_call}

def ocr_step(state:OCRAgentState):
    extracted_text = textract_service(state["file"])
    print("Extract text")   
    return{"messages":state["messages"],"extracted_text":extracted_text}

# Graph Builder
def graph_builder(image_bytes):
    workflow = StateGraph(OCRAgentState)

    workflow.add_node("schema",schematizer)
    workflow.add_node("ocr",ocr_step)
    workflow.add_node("classify",classifier) 

    tool_node = ToolNode(tools=[tank_schematizer,oxxo_schematizer])
    workflow.add_node("tools",tool_node)
    workflow.add_conditional_edges("schema",tools_condition)

    workflow.add_edge(START,"ocr")
    workflow.add_edge("ocr","classify")
    workflow.add_edge("classify","schema")    
    workflow.add_edge("tools","schema")
    
    ocr_agent = workflow.compile()

    message = [
        SystemMessage(content=(
        "You are an agent responsible for analyzing texts extracted via OCR and processing them based on their content."            
    ))]

    initial_state={
        "messages":message,
        "file":image_bytes,  
    }

    final_state=ocr_agent.invoke(initial_state)  

    return {"raw_text":final_state["extracted_text"],
            "struct_text":final_state["structured_text"]}