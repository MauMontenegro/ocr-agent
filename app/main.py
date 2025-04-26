import redis
from fastapi import FastAPI
from app.routers.ocr import router as ocr_router
from app.routers.converse import router as converse_router

app = FastAPI(title="Agente Tickets-OCR Petroil",version="1.0")

app.state.redis_client = redis.Redis(host="localhost", port=6379, db=0)

app.include_router(ocr_router, prefix="/ocr", tags=["OCR"])
app.include_router(converse_router,prefix="/converse",tags=["Chat"])

@app.get("/")
def init_page():
    """
        Punto de entrada para el Agente de OCR.
        Determina si el servicio está Online.
    """
    return {"message":"El servicio de OCR está Operativo"}   