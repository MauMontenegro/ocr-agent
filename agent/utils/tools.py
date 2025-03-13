"""
    Modulo que contiene las herramientas utilizadas por el Agente de OCR
"""
import os
from langchain_core.tools import tool
from dotenv import load_dotenv
from langchain_aws import ChatBedrockConverse

load_dotenv()

def general_schematizer(ocr_text:str,schema:dict,task_description:str,additional:str)-> str:
    MODEL_ID = os.getenv("MODEL_ID")
    llm_schema = ChatBedrockConverse(model_id = MODEL_ID)

    schematizer_prompt = f"""{task_description}

    OCR_TEXT:
    {ocr_text}

    Schema:
    {schema}

    {additional}
    """
    schema_response = llm_schema.invoke(schematizer_prompt)

    return "Done"