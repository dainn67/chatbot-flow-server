from fastapi import APIRouter, Body
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional
import asyncio
from app.services.llm_service import stream_llm

stream_router = APIRouter()


class StreamRequest(BaseModel):
    user_input: str
    provider: Optional[str] = "gemini"  # "gemini" or "openai"


async def event_stream():
    """Demo event stream"""
    for i in range(5):
        yield f"data: message {i}\n\n"
        await asyncio.sleep(1)


@stream_router.get("/sse")
async def sse():
    """Demo SSE endpoint"""
    return StreamingResponse(event_stream(), media_type="text/event-stream")


@stream_router.post("/chat")
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
