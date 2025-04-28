import json
from fastapi import HTTPException, APIRouter,Request
from fastapi.responses import StreamingResponse
from app.agent.utils.schemas import userQuery
from app.agent.converse_agent import converse_agent_streamer

router = APIRouter()

@router.post("/chat")
async def converse(request:Request,query: userQuery):
    """
    Llamada al agente conversacional OCR with streaming
    """
    print("query: ", query.user_query)
    session_id = query.user_id
    user_query = query.user_query
    redis_client = request.app.state.redis_client
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
