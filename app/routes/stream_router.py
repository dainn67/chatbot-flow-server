from fastapi import APIRouter, Body
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional
from app.services.llm_service import stream_llm

stream_router = APIRouter()

class StreamRequest(BaseModel):
    user_input: str
    provider: Optional[str] = "gemini"  # "gemini" or "openai"


@stream_router.post("/ask")
async def stream_chat(request: StreamRequest = Body(...)):
    """
    Stream chat response from LLM using Server-Sent Events (SSE).
    
    Example request body:
    {
        "user_input": "Xin chào, bạn có khỏe không?",
        "provider": "gemini"
    }
    
    Response format: SSE stream with JSON data:
    data: {"chunk": "text chunk", "done": false}
    data: {"chunk": "", "done": true}
    """
    return StreamingResponse(
        stream_llm(request.provider, request.user_input),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        }
    )
