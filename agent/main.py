from fastapi import FastAPI, UploadFile, File, HTTPException
from agent.services.ocr_agent import graph_builder
from agent.utils.schemas import userQuery
import logging

# Explicitly configure logging
logging.basicConfig(
    level=logging.DEBUG,  # Change to DEBUG to see everything
    format="%(asctime)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)

app = FastAPI(title="Agente Tickets-OCR Petroil",version="1.0")

@app.get("/")
def init_page():
    """
        Punto de entrada para el Agente de OCR.
        Determina si el servicio está Online.
    """
    return {"message":"El servicio está Operativo"}

@app.post("/agent")
async def agent_call(file:UploadFile=File(...) ):
    """
        Llamada al agente de ocr y estructuración
    """
    print(file)
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(
            status_code=400, detail="Only JPEG and PNG files are allowed."
        )
    file_bytes = await file.read()       
   
    response = graph_builder(file_bytes)

    return {"raw_text":response["raw_text"],
            "structured_text":response["struct_text"]}

@app.post("/chat")
async def converse(query:userQuery):
    """
        Llamada al agente conversacional OCR
    """
    
    pass