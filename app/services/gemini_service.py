import google.generativeai as genai
import os
import asyncio
from concurrent.futures import ThreadPoolExecutor
from app.core.config import settings
from typing import AsyncGenerator

genai.configure(api_key=settings.GEMINI_API_KEY)

# Thread pool để chạy synchronous Gemini calls
executor = ThreadPoolExecutor(max_workers=5)


async def call_gemini(prompt: str, model: str = "gemini-2.0-flash-exp") -> str:
    """
    Async call to Google Gemini model using thread pool for sync API.

    Args:
        prompt: The user prompt/question for Gemini.
        model: The Gemini model to use (default is "gemini-2.0-flash-exp").

    Returns:
        The generated response text from Gemini.
    """
    # Get the current running event loop
    loop = asyncio.get_running_loop()
    
    # Define a synchronous function to call the Gemini API
    def _call():
        # Create the generative model instance
        model_instance = genai.GenerativeModel(model)
        # Call generate_content to get a response (this is synchronous)
        response = model_instance.generate_content(prompt)
        # Return only the text part of the response
        return response.text

    # Run the synchronous Gemini call in a thread pool to avoid blocking the main event loop
    result = await loop.run_in_executor(executor, _call)
    return result


async def stream_gemini(prompt: str, model: str = "gemini-2.0-flash-exp") -> AsyncGenerator[str, None]:
    """
    Stream Google Gemini model response with a simple prompt.
    Yields chunks of text as they arrive from the API.
    Optimized to efficiently bridge sync generator to async generator.
    
    Args:
        prompt: The user prompt/question for Gemini.
        model: The Gemini model to use (default is "gemini-2.0-flash-exp").
        
    Yields:
        Text chunks as they arrive from the API.
    """
    loop = asyncio.get_running_loop()

    def get_text_chunks():
        response = genai.GenerativeModel(model).generate_content(
            prompt,
            stream=True
        )
        return (chunk.text for chunk in response if getattr(chunk, "text", None))

    # We have to consume the generator synchronously in a thread and forward chunks to async world.
    queue = asyncio.Queue()

    def generator_worker():
        try:
            for chunk in get_text_chunks():
                asyncio.run_coroutine_threadsafe(queue.put(chunk), loop)
        finally:
            asyncio.run_coroutine_threadsafe(queue.put(None), loop)

    # Launch generator_worker in a thread WITHOUT awaiting it (non-blocking)
    # This allows us to start yielding chunks immediately as they arrive
    loop.run_in_executor(executor, generator_worker)

    # Yield items as soon as they are available from the queue
    while True:
        chunk = await queue.get()
        if chunk is None:
            break
        yield chunk
