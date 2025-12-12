from app.services.llm_service import run_llm
from fastapi import APIRouter, Body
from pydantic import BaseModel
from app.flows.question_chatbot import run_single_question

single_question_router = APIRouter()

class QuestionRequest(BaseModel):
    user_input: str
    provider: str = "openai"

@single_question_router.post("/ask")
async def ask_single_question(request: QuestionRequest = Body(...)):
    """
    Ask a single question to the LLM.
    """
    result = await run_llm(request.provider, request.user_input)
    return result