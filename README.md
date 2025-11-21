# Chatbot Flow Server

Server API cho quản lý chatbot flows với tích hợp LLM (OpenAI, Gemini).

## 🚀 Khởi động nhanh

### 1. Cài đặt dependencies

```bash
# Tạo virtual environment (nếu chưa có)
python -m venv venv

# Kích hoạt virtual environment
# macOS/Linux:
source venv/bin/activate
# Windows:
# venv\Scripts\activate

# Cài đặt packages
pip install -r requirements.txt
```

### 2. Cấu hình môi trường

Tạo file `.env` trong thư mục gốc:

```env
OPENAI_API_KEY=your_openai_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
```

### 3. Chạy server

```bash
# Development mode với auto-reload
uvicorn app.main:app --reload

# Hoặc chạy trực tiếp
python -m app.main
```

Server sẽ chạy tại: http://localhost:8000

## 📚 API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🏗️ Cấu trúc dự án

```
chatbot-flow-server/
├── app/
│   ├── __init__.py           # Package initialization
│   ├── main.py               # FastAPI app entry point
│   ├── core/
│   │   └── config.py         # Configuration settings
│   ├── services/
│   │   ├── llm_service.py    # LLM service interface
│   │   ├── openai_service.py # OpenAI integration
│   │   └── gemini_service.py # Gemini integration
│   └── flows/
│       └── question_chatbot.py # Chatbot flow logic
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables (tạo thủ công)
└── README.md
```

## 🔧 API Endpoints

### Health Check

- `GET /` - Root health check
- `GET /health` - Detailed health status

## 📝 Ghi chú

- Đảm bảo đã cấu hình API keys trong file `.env`
- Server chạy ở port 8000 theo mặc định
- CORS được cấu hình để chấp nhận tất cả origins (nên giới hạn trong production)
