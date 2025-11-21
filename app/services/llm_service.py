from app.services.openai_service import call_gpt
from app.services.gemini_service import call_gemini

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
