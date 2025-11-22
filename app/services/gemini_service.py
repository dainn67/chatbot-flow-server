import google.generativeai as genai
import os
import asyncio
from concurrent.futures import ThreadPoolExecutor
from app.core.config import settings
from typing import AsyncGenerator

genai.configure(api_key=settings.GEMINI_API_KEY)

# Thread pool để chạy synchronous Gemini calls
executor = ThreadPoolExecutor(max_workers=5)

def _call_gemini_sync(prompt: str, model: str) -> str:
    """
    Synchronous call to Gemini API.
    """
    response = genai.GenerativeModel(model).generate_content(prompt)
    return response.text

async def call_gemini(prompt: str, model: str = "gemini-2.0-flash-exp") -> str:
    """
    Call Google Gemini model with a simple prompt (async wrapper).
    """
    print(f"Calling Gemini model: {model} with prompt: {prompt}")
    
    # Chạy synchronous call trong thread pool
    loop = asyncio.get_event_loop()
    response_text = await loop.run_in_executor(
        executor, 
        _call_gemini_sync,
        prompt,
        model
    )
    return response_text


def _stream_gemini_sync(prompt: str, model: str):
    """
    Synchronous streaming call to Gemini API.
    Returns a generator of text chunks.
    """
    response = genai.GenerativeModel(model).generate_content(
        prompt,
        stream=True
    )
    for chunk in response:
        if chunk.text:
            yield chunk.text


async def stream_gemini(prompt: str, model: str = "gemini-2.0-flash-exp") -> AsyncGenerator[str, None]:
    """
    Stream Google Gemini model response with a simple prompt.
    Yields chunks of text as they arrive from the API.
    """
    print(f"Streaming Gemini model: {model} with prompt: {prompt}")
    
    # Chạy synchronous streaming call trong thread pool
    loop = asyncio.get_event_loop()
    
    # Tạo generator từ sync function
    def run_sync_stream():
        return _stream_gemini_sync(prompt, model)
    
    sync_gen = await loop.run_in_executor(executor, run_sync_stream)
    
    # Convert sync generator to async generator
    for chunk in sync_gen:
        yield chunk
        await asyncio.sleep(0)  # Cho phép event loop xử lý các tasks khác
