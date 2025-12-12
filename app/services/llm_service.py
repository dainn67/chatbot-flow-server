from app.services.openai_service import call_gpt
from app.services.gemini_service import call_gemini, stream_gemini
from typing import AsyncGenerator

async def run_llm(provider: str, prompt: str) -> str:
    """
    provider = "openai" or "gemini"
    """
    if provider == "openai":
        return await call_gpt(prompt)
    elif provider == "gemini":
        return await call_gemini(prompt)
    else:
        raise ValueError(f"Unknown provider: {provider}")


async def stream_llm(provider: str, prompt: str) -> AsyncGenerator[str, None]:
    """
    Stream LLM response based on provider.
    provider = "openai" or "gemini"
    Yields text chunks as they arrive.
    """
    if provider == "openai":
        async for chunk in stream_gpt(prompt):
            yield chunk
    elif provider == "gemini":
        async for chunk in stream_gemini(prompt):
            yield chunk
    else:
        raise ValueError(f"Unknown provider: {provider}")
