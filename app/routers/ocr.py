import json
import requests
from PIL import Image
import io
from fastapi import UploadFile, File, HTTPException, APIRouter,Request
from app.agent.ocr_agent import graph_builder


router= APIRouter()

@router.post("/upload")
async def agent_call(request:Request,file:UploadFile=File(...)):
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
    redis_client=request.app.state.redis_client
    redis_client.set(session_id, json.dumps(response["raw_text"]))

    return {"structured_text":response["struct_text"]}

@router.post("/upload_url")
async def agent_call_url(data:dict):
    """
        Llamada al agente de ocr y estructuración mediente una url
    """
    image_url = data.get("image_url")
    if not image_url:
        raise HTTPException(status_code=400, detail="No image_url provided.")
    
    response = requests.get(image_url,timeout=20)
    image = Image.open(io.BytesIO(response.content))

    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='JPEG')
    file_bytes = img_byte_arr.getvalue()          
    try:
        response = graph_builder(file_bytes)
        return {"structured_text":response["struct_text"]}
    except Exception as e:
        custom_json = {
            "date": "None",
            "address": "None",
            "station": "None",
            "total": 0,
            "quantity": 0
             }
        print(f"Error in general_schematizer: {str(e)}")
        return{"structured:text":custom_json}
    