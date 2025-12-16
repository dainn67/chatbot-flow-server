from app.services.llm_service import run_llm
from fastapi import APIRouter, Body
from pydantic import BaseModel
import json

single_question_router = APIRouter()

class QuestionRequest(BaseModel):
    user_input: str
    provider: str = "openai"

@single_question_router.post("/suggest-topic")
async def suggest_topic(request: QuestionRequest = Body(...)):
    """
    Ask a single question to the LLM.
    """
    result = await run_llm(request.provider, request.user_input)

    output_text = result.get("message")

    json_output = json.loads(output_text.replace('```json', '').replace('```', ''))

    return {
        "id": json_output.get("id"),
        "reason": json_output.get("reason"),
        "token_logs": result.get("token_logs")
    }

@single_question_router.post("/analyze-progress")
async def analyze_progress(request: QuestionRequest = Body(...)):
    """
    Analyze the progress of the user.
    """
    result = await run_llm(request.provider, request.user_input)

    analyzed_progress = result.get("message")
    token_logs = result.get("token_logs")

    return {
        "analyzed_progress": analyzed_progress,
        "token_logs": token_logs
    }