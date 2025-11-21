import google.generativeai as genai
import os
import asyncio
from concurrent.futures import ThreadPoolExecutor
from app.core.config import settings

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
