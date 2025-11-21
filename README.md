# Chatbot Flow Server

Server API cho quản lý chatbot flows với tích hợp LLM (OpenAI, Google Gemini).

## ✨ Tính năng

- 🤖 Tích hợp nhiều LLM providers (OpenAI GPT, Google Gemini)
- ⚡ Async/await support cho performance tốt
- 🔄 Thread pool executor cho Gemini API
- 📝 API documentation tự động với Swagger UI
- 🔒 Environment-based configuration
- 🌐 CORS support

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
│   ├── routes/
│   │   └── flow.py           # Flow API routes
│   ├── services/
│   │   ├── llm_service.py    # LLM service interface
│   │   ├── openai_service.py # OpenAI GPT integration
│   │   └── gemini_service.py # Google Gemini integration
│   └── flows/
│       └── question_chatbot.py # Chatbot flow logic
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables (tạo thủ công)
└── README.md
```

## 🔧 API Endpoints

### Health Check

- **GET** `/` - Root health check
- **GET** `/health` - Detailed health status (kiểm tra cấu hình API keys)

### Chatbot Flows

- **POST** `/api/flows/ask` - Gửi câu hỏi đến chatbot

**Request body:**
```json
{
  "user_input": "Xin chào, bạn có khỏe không?"
}
```

**Response:**
```json
{
  "user_input": "Xin chào, bạn có khỏe không?",
  "llm_response": "Câu trả lời từ LLM..."
}
```

## 🛠️ Tech Stack

- **Framework**: FastAPI 0.104.1
- **Server**: Uvicorn
- **LLM Integrations**:
  - OpenAI API 1.3.0
  - Google Generative AI 0.8.5
- **Python**: 3.8+

## 📝 Ghi chú

- Đảm bảo đã cấu hình API keys trong file `.env`
- Server chạy ở port 8000 theo mặc định
- CORS được cấu hình để chấp nhận tất cả origins (nên giới hạn trong production)
- Gemini API sử dụng thread pool executor để xử lý async calls
- Mặc định sử dụng model `gemini-2.0-flash-exp`

## 🐛 Troubleshooting

### Import error "google.generativeai could not be resolved"

1. Đảm bảo đã cài đặt dependencies: `pip install -r requirements.txt`
2. Kiểm tra đã activate virtual environment
3. Khởi động lại IDE để nhận diện lại Python interpreter
4. Chọn đúng Python interpreter: `./venv/bin/python`

### API Key errors

Kiểm tra file `.env` đã được tạo và có đúng API keys. Truy cập `/health` để xem trạng thái cấu hình.
