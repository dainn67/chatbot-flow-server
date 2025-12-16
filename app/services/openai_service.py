from openai import OpenAI
from app.core.config import settings
import json

client = OpenAI(api_key=settings.OPENAI_API_KEY)

async def call_gpt(prompt: str, model: str = "gpt-4o-mini"):
    completion = client.responses.create(
        model=model,
        input=prompt
    )

    # Extract tokens exactly following your API's response schema
    output_text = completion.output_text
    usage = completion.usage

    token_logs = {
        "input_tokens": usage.input_tokens,
        "output_tokens": usage.output_tokens,
        "total_tokens": usage.total_tokens
    }

    return {
        "message": output_text,
        "token_logs": token_logs
    }
