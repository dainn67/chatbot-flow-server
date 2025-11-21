from fastapi import APIRouter
from app.flows.question_chatbot import run_test_workflow

router = APIRouter()

@router.post("/ask")
def ask_question(user_input: str):
    """
    Simple API that runs a test workflow calling Gemini.
    """
    result = run_test_workflow(user_input)
    return result
