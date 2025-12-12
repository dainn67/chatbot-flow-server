from app.services.llm_service import run_llm

async def run_test_workflow(user_input: str) -> dict:
    """
    Example workflow that asks Gemini a question.
    """

    prompt = f"You are a helpful assistant. The user says: {user_input}. Respond politely."

    answer = await run_llm("gemini", prompt)

    return {
        "input": user_input,
        "response": answer
    }

async def run_single_question(user_input: str) -> dict:
    """
    Run a single question workflow.
    """
    import json
    answer = await run_llm("openai", user_input)
    print(answer)
    try:
        decoded_answer = json.loads(answer)
        return decoded_answer
    except json.JSONDecodeError as e:
        return {"error": f"Failed to decode JSON: {str(e)}", "raw_response": answer}