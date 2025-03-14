from fastapi import FastAPI, UploadFile, File, HTTPException
from agent.services.textract import textract_service
from agent.services.ocr_agent import graph_builder

app = FastAPI(title="Agente Tickets-OCR Petroil",version="1.0")

@app.get("/")
def init_page():
    """
        Punto de entrada para el Agente de OCR.
        Determina si el servicio está Online.
    """
    return {"message":"El servicio está Operativo"}

@app.post("/process")
async def agent_call(file:UploadFile=File(...) ):
    """
        Endpoint que maneja llamadas al agente de OCR
    """
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(
            status_code=400, detail="Only JPEG and PNG files are allowed."
        )
    file_bytes = await file.read()
    response = textract_service(file_bytes)
    returnal = graph_builder(response)

    return {"response":returnal}