"""
    Modulo que contiene las herramientas utilizadas por el Agente de OCR
"""
import os
import traceback
from dotenv import load_dotenv
from langchain_aws import ChatBedrockConverse
from app.agent.utils.prompts import classifier_prompt

load_dotenv()

def general_schematizer(ocr_text:str,task_description:str,doc_type:str,output_schema)-> str:        

    MODEL_ID = os.getenv("MODEL_ID_SCHEMA")
    llm_schema = ChatBedrockConverse(model_id = MODEL_ID)
        
    # Configure the model to use structured output
    structured_llm = llm_schema.with_structured_output(output_schema)

    schematizer_prompt = f"""{task_description}
    OCR_TEXT:
    {ocr_text}   
    """    
   
    print(f"Esquematizando texto para {doc_type}...")
    try:
        # Get the response from the LLM using structured output
        response = structured_llm.invoke(schematizer_prompt)               

        # Save to JSON file (fix for Pydantic v2)
        with open(f"cleaned_{doc_type}.json", "w", encoding="utf-8") as f:            
            if hasattr(response, "model_dump_json"):
                f.write(response.model_dump_json(indent=4))

        print(f"Schema saved successfully as cleaned_{doc_type}.json")        
        
        return "Done",response
        
    except Exception as e:        
        traceback.print_exc()
        print(f"Error in general_schematizer: {str(e)}")
        
        # If everything fails, save the raw response for debugging
        with open(f"error_{doc_type}_response.txt", "w", encoding="utf-8") as f:
            f.write(str(response) if 'response' in locals() else "No response")

        return "Not Done"
        

def classify(ocr_text:str)-> str:
    """
    Classify ocr texts based on their content
    """
    MODEL_ID = os.getenv("MODEL_ID_CLASSIFY")
    llm_classify = ChatBedrockConverse(model_id = MODEL_ID)

    classification_message = f"{classifier_prompt}\n\nOCR Text:\n{ocr_text}"
    classification_response = llm_classify.invoke(classification_message)

    return classification_response
