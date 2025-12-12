from app.services.gemini_service import call_gemini

async def main_chabot_flow(user_input: str) -> dict:
    """
    Main chatbot flow
    """

    prompt = f"You are a helpful assistant. The user says: {user_input}. Respond politely."

    answer = await call_gemini(prompt)

    return {
        "input": user_input,
        "response": answer
    }
