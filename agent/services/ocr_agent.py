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
from agent.utils.tools import general_schematizer,classify
from agent.utils.prompts import(tank_task_prompt,purchase_ticket_task_prompt,edenred_task_prompt)

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


from agent.utils.schemas import TankResponse,EdenredReceipt,TicketReceipt
@tool
def tank_schematizer(ocr_text: str) -> str:
    """Structure a text that defines the state of gasoline tanks.
    The tanks can have the following features: Volúmen, temperatura, etc.
    """
    print("Usando Tool de Tanques.", flush=True)
    response,schema = general_schematizer(
        ocr_text=ocr_text,       
        task_description=tank_task_prompt,        
        output_schema=TankResponse,
        doc_type="fuel_tank")    
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
def edenred_schematizer(ocr_text: str) -> str:
    """Structure a text that defines a Edenred Transport Unit Purchase Receipt.
    """
    print("Usando Tool de Edenred.", flush=True)
    response,schema = general_schematizer(
        ocr_text=ocr_text,       
        task_description=edenred_task_prompt,        
        output_schema=EdenredReceipt,
        doc_type="edenred_receipt")    
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
    """Structure a text that defines a purchase ticket for selled products in a convenience store.      
    """
    print("Calling Purchase Ticket Tool.")
    response,schema = general_schematizer(
        ocr_text=ocr_text,       
        task_description=purchase_ticket_task_prompt,        
        output_schema=TicketReceipt,
        doc_type="purchase_ticket")
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
    

tools=[tank_schematizer,oxxo_schematizer,edenred_schematizer]

# Bind Tools to Agent
llm_w_tools = llm.bind_tools(tools)

tool_node = ToolNode(tools)

# Definition of nodes (operations on states)

def build_schematizer_tool(state:OCRAgentState):
    print("Building Schematizer Tool...")

    ocr_text = state["extracted_text"]
    full_ocr_text = "\n".join(ocr_text)

    chosen_tool = state["tool_t_call"]    
    chosen_tool = chosen_tool.strip().strip('"\'')     
    message_w_tool_call=AIMessage(
                                    content="",
                                    tool_calls=[
                                        {
                                            "name": chosen_tool,
                                            "args": {"ocr_text": full_ocr_text},            
                                            "type": "tool_call",
                                            "id": "1234",
                                        }
                                    ],
                                )
    return {"messages":[message_w_tool_call]}

def schematizer(state:OCRAgentState):      
    if isinstance(state["messages"][-1], ToolMessage) and "Done" in state["messages"][-1].content:
        return state
    
    response = tool_node.invoke({"messages": state["messages"]})     
    
    if isinstance(response[0],Command):        
        updates = response[0].update           
        return {"messages":updates["messages"][-1],"structured_text":updates["structured_text"]}    
    return {"messages":state["messages"]}    

def classifier(state:OCRAgentState):
    print("Cassifying Document")
    sample_length = min(len("\n".join(state["extracted_text"])), 1000) 
    doc_type = classify(state["extracted_text"][:sample_length])
    tool_t_call = doc_type.content.strip().lower()    
    return{"messages":state["messages"],"tool_t_call":tool_t_call}

def ocr_step(state:OCRAgentState):
    try:
        extracted_text = textract_service(state["file"])
        print("Extracting Text")
        return {"messages": state["messages"], "extracted_text": extracted_text}
    except Exception as e:
        logger.error(f"OCR extraction failed: {str(e)}")
        return {"messages": state["messages"], "extracted_text": [], "error": str(e)}

# Graph Builder
def graph_builder(image_bytes):
    workflow = StateGraph(OCRAgentState)

    workflow.add_node("schema",schematizer)
    workflow.add_node("ocr",ocr_step)
    workflow.add_node("classify",classifier)
    workflow.add_node("build_schematizer",build_schematizer_tool)

    tool_node = ToolNode(tools=tools)
    workflow.add_node("tools",tool_node)
    workflow.add_conditional_edges("schema",tools_condition)

    workflow.add_edge(START,"ocr")
    workflow.add_edge("ocr","classify")
    workflow.add_edge("classify","build_schematizer")
    workflow.add_edge("build_schematizer","schema")    
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