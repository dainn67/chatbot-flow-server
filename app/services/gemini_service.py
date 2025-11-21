import google.generativeai as genai
import os
from app.core.config import settings

genai.configure(api_key=settings.GEMINI_API_KEY)

async def call_gemini(prompt: str, model: str = "gemini-2.0-flash") -> str:
    """
    Call Google Gemini model with a simple prompt.
    """
    response = genai.GenerativeModel(model).generate_content(prompt)
    return response.text
