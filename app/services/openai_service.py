from openai import OpenAI
import os
from app.core.config import settings
from typing import AsyncGenerator

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


async def stream_gpt(prompt: str, model: str = "gpt-4o-mini") -> AsyncGenerator[str, None]:
    """
    Stream GPT model response with a simple user prompt.
    Yields chunks of text as they arrive from the API.
    """
    stream = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        stream=True
    )
    
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            yield chunk.choices[0].delta.content
