""""
    Modulo que contiene el estado del Agente OCR
"""

from typing import Annotated,Optional
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages
from pydantic import BaseModel

class OCRAgentState(TypedDict):
    file : Optional[bytes]
    messages : Annotated[list,add_messages]
    extracted_text: Optional[str]    
    tool_t_call: Optional[str]
    structured_text: Optional[BaseModel|None]