""""
    Modulo que contiene el estado del Agente OCR
"""

from typing import Annotated,Optional
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages


class OCRAgentState(TypedDict):
    """
    Define el estado del Agente OCR
    """
    messages = Annotated[list,add_messages]