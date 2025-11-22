from app.services.llm_service import stream_llm
from typing import AsyncGenerator

async def run_stream_test_workflow(user_input: str, provider: str = "gemini") -> AsyncGenerator[str, None]:
    """
    Example streaming workflow that asks an LLM a question and streams the response.
    
    Args:
        user_input: The user's question/input
        provider: "gemini" or "openai"
    
    Yields:
        Text chunks as they arrive from the LLM
    """
    prompt = f"You are a helpful assistant. The user says: {user_input}. Respond politely and helpfully."
    
    async for chunk in stream_llm(provider, prompt):
        yield chunk

