from fastapi import FastAPI, UploadFile, File, HTTPException
from agent.services.textract import textract_service
from langchain_core.messages import HumanMessage, SystemMessage
from agent.services.ocr_agent import graph_builder
app = FastAPI(title="Agente OCR Petroil",version="1.0")

@app.get("/")
def init_page():
    """
        Punto de entrada para el Agente de OCR.
        Determina si el servicio está Online.
    """
    return {"message":"El servicio está Operativo"}

@app.post("/process")
def agent_call(file:UploadFile=File(...) ):
    """
        Endpoint que maneja llamadas al agente de OCR
    """
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(
            status_code=400, detail="Only JPEG and PNG files are allowed."
        )
    
    response = textract_service(file.read())
    ocr_agent = graph_builder()

    message = [
        SystemMessage(content=(
        "You are an agent responsible for analyzing texts extracted via OCR and processing them based on their content."    
    )),
        HumanMessage(content=f"This is the OCR text:{response}")]

    initial_state={
        "messages":message,  
    }

    ocr_agent.invoke(initial_state)
    
