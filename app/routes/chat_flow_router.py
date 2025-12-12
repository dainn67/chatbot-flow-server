from app.services.llm_service import run_llm
from fastapi import APIRouter, Body
from pydantic import BaseModel
from app.flows.question_chatbot import run_test_workflow

chat_flow_router = APIRouter()

class QuestionRequest(BaseModel):
    user_input: str
    provider: str = "gemini"

@chat_flow_router.post("/ask")
async def ask_chat_flow(request: QuestionRequest = Body(...)):
    """
    Run a chatbot flow.
    """
    result = await run_llm(request.provider, request.user_input)
    return result