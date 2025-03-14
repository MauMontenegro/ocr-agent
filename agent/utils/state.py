""""
    Modulo que contiene el estado del Agente OCR
"""

from typing import Annotated,Optional
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages


class OCRAgentState(TypedDict):
    file : Optional[bytes]
    messages : Annotated[list,add_messages]
    extracted_text: Optional[str]
    status: Optional[str]
    document_type: Optional[str]