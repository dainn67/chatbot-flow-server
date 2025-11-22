from fastapi import APIRouter, Body
from pydantic import BaseModel
from app.flows.question_chatbot import run_test_workflow

flow_router = APIRouter()

class FlowRequest(BaseModel):
    user_input: str

@flow_router.post("/ask")
async def ask_question(request: FlowRequest = Body(...)):
    """
    Simple API that runs a test workflow calling Gemini.
    
    Example request body:
    {
        "user_input": "Xin chào, bạn có khỏe không?"
    }
    """
    try:
        result = await run_test_workflow(request.user_input)
        return result
    except Exception as e:
        return {
            "error": str(e),
            "message": "Có lỗi xảy ra khi xử lý request. Vui lòng kiểm tra API key hoặc cấu hình."
        }
