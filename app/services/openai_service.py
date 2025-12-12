from openai import OpenAI
from app.core.config import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)

async def call_gpt(prompt: str, model: str = "gpt-4o-mini") -> str:
    """
    Call GPT model with a simple user prompt.
    """
    completion = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )

    return completion.choices[0].message.content
