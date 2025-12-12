from fastapi import APIRouter
from pydantic import BaseModel
from app.flows.question_chatbot import run_test_workflow, run_single_question

router = APIRouter()

class QuestionRequest(BaseModel):
    user_input: str

@router.post("/ask")
async def ask_question(request: QuestionRequest):
    """
    Simple API that runs a test workflow calling Gemini.
    """
    result = await run_test_workflow(request.user_input)
    return result

@router.post("/ask-single")
async def ask_single_question(request: QuestionRequest):
    """
    Simple API that runs a single question workflow.
    """
    result = await run_single_question(request.user_input)
    return result