from fastapi import FastAPI, UploadFile, File, HTTPException
from agent.services.ocr_agent import graph_builder
from agent.services.converse_agent import converse_agent_streamer
from agent.utils.schemas import userQuery
import logging
import redis
import json

# Explicitly configure logging
logging.basicConfig(
    level=logging.DEBUG,  # Change to DEBUG to see everything
    format="%(asctime)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)

redis_client = redis.Redis(host="localhost", port=6379, db=0)

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
    
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(
            status_code=400, detail="Only JPEG and PNG files are allowed."
        )
    file_bytes = await file.read()       
   
    response = graph_builder(file_bytes)

    session_id = file.filename
    redis_client.set(session_id, json.dumps(response["raw_text"]))

    return {"raw_text":response["raw_text"],
            "structured_text":response["struct_text"]}

from fastapi.responses import StreamingResponse
import asyncio


@app.post("/chat")
async def converse(query: userQuery):
    """
    Llamada al agente conversacional OCR with streaming
    """
    print("query: ", query.user_query)
    session_id = query.user_id
    user_query = query.user_query
    extracted_data_json = redis_client.get(session_id)
   
    if not extracted_data_json:
        raise HTTPException(status_code=404, detail="Session not found. Upload an image first.")
    
    extracted_data = json.loads(extracted_data_json)
    prompt = f"Extracted data: {extracted_data}\n\nQuestion: {user_query}"
    
    # Return a streaming response
    return StreamingResponse(
        converse_agent_streamer(prompt),
        media_type="text/event-stream"
    )


    
   