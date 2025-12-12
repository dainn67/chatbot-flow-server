"""
Main FastAPI application entry point
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.routes.stream_router import stream_router
from app.routes.chat_flow_router import chat_flow_router
from app.routes.single_question_router import single_question_router

# Khởi tạo FastAPI app
app = FastAPI(
    title="Chatbot Flow Server",
    description="API server cho quản lý chatbot flows với tích hợp LLM",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Cấu hình CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Trong production nên giới hạn origins cụ thể
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/", tags=["Health"])
async def root():
    """
    Health check endpoint
    """
    return {
        "status": "ok",
        "message": "Chatbot Flow Server đang hoạt động",
        "version": "0.1.0"
    }

@app.get("/health", tags=["Health"])
async def health_check():
    """
    Detailed health check endpoint
    """
    return {
        "status": "healthy",
        "service": "chatbot-flow-server",
        "openai_configured": bool(settings.OPENAI_API_KEY),
        "gemini_configured": bool(settings.GEMINI_API_KEY)
    }

# Startup event
@app.on_event("startup")
async def startup_event():
    """
    Chạy khi server khởi động
    """
    print("🚀 Chatbot Flow Server đang khởi động...")
    print(f"📝 Docs: http://localhost:3000/docs")
    print(f"🔧 ReDoc: http://localhost:3000/redoc")
    
    # Kiểm tra cấu hình
    if not settings.OPENAI_API_KEY or not  settings.GEMINI_API_KEY:
        if not settings.OPENAI_API_KEY:
            print("⚠️ OPENAI_API_KEY not configured")
        else:
            print("⚠️ GEMINI_API_KEY not configured")
        

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """
    Chạy khi server tắt
    """
    print("👋 Chatbot Flow Server đang tắt...")


app.include_router(stream_router, prefix="/api/stream", tags=["Stream"])
app.include_router(chat_flow_router, prefix="/api/chat-flow", tags=["Chat Flow"])
app.include_router(single_question_router, prefix="/api/single-question", tags=["Single Question"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=3000,
        reload=True
    )
