from fastapi import APIRouter
from fastapi.responses import StreamingResponse
import asyncio

stream_router = APIRouter()

async def event_stream():
    for i in range(5):
        yield f"data: message {i}\n\n"
        await asyncio.sleep(1)

@stream_router.get("/sse")
async def sse():
    return StreamingResponse(event_stream(), media_type="text/event-stream")
