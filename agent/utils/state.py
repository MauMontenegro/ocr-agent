""""
    Modulo que contiene el estado del Agente OCR
"""

from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages


class OCRAgentState(TypedDict):
    messages : Annotated[list,add_messages]