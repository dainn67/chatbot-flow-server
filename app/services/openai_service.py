from openai import AsyncOpenAI
from concurrent.futures import ThreadPoolExecutor
from app.core.config import settings
from typing import AsyncGenerator

# Sử dụng AsyncOpenAI client thay vì sync client
client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

# Thread pool executor cho fallback nếu cần
executor = ThreadPoolExecutor(max_workers=5)

async def call_gpt(prompt: str, model: str = "gpt-4o-mini") -> str:
    """
    Async call to GPT model with a simple user prompt.
    Uses native async OpenAI client to avoid blocking the event loop.
    
    Args:
        prompt: The user prompt/question for GPT.
        model: The GPT model to use (default is "gpt-4o-mini").
        
    Returns:
        The generated response text from GPT.
    """
    completion = await client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )

    return completion.choices[0].message.content


async def stream_gpt(prompt: str, model: str = "gpt-4o-mini") -> AsyncGenerator[str, None]:
    """
    Stream GPT model response with a simple user prompt.
    Yields chunks of text as they arrive from the API.
    Uses native async OpenAI client for efficient non-blocking streaming.
    
    Args:
        prompt: The user prompt/question for GPT.
        model: The GPT model to use (default is "gpt-4o-mini").
        
    Yields:
        Text chunks as they arrive from the API.
    """
    stream = await client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        stream=True
    )
    
    async for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            yield chunk.choices[0].delta.content
