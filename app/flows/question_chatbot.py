from app.services.gemini_service import call_gemini

async def run_test_workflow(user_input: str) -> dict:
    """
    Example workflow that asks Gemini a question.
    """

    prompt = f"You are a helpful assistant. The user says: {user_input}. Respond politely."

    answer = await call_gemini(prompt)

    return {
        "input": user_input,
        "response": answer
    }
