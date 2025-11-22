# 🚀 Hướng dẫn Streaming API

## Tổng quan

Server này hỗ trợ streaming responses từ cả **Google Gemini** và **OpenAI GPT** thông qua Server-Sent Events (SSE).

## Các tính năng đã thêm

### 1. **Streaming Functions**

#### OpenAI GPT Streaming
```python
from app.services.openai_service import stream_gpt

async for chunk in stream_gpt("Your prompt here"):
    print(chunk, end='', flush=True)
```

#### Gemini Streaming
```python
from app.services.gemini_service import stream_gemini

async for chunk in stream_gemini("Your prompt here"):
    print(chunk, end='', flush=True)
```

#### Unified LLM Streaming
```python
from app.services.llm_service import stream_llm

# Sử dụng với Gemini
async for chunk in stream_llm("gemini", "Your prompt"):
    print(chunk, end='', flush=True)

# Sử dụng với OpenAI
async for chunk in stream_llm("openai", "Your prompt"):
    print(chunk, end='', flush=True)
```

### 2. **Stream Test Flow**

File `app/flows/stream_test_flow.py` cung cấp workflow ví dụ:

```python
from app.flows.stream_test_flow import run_stream_test_workflow

async for chunk in run_stream_test_workflow("Hello!", provider="gemini"):
    print(chunk, end='', flush=True)
```

### 3. **API Endpoints**

#### POST /api/stream/chat

Stream chat response với request body:

```bash
curl -X POST http://localhost:8000/api/stream/chat \
  -H "Content-Type: application/json" \
  -d '{
    "user_input": "Xin chào, bạn có khỏe không?",
    "provider": "gemini"
  }'
```

#### GET /api/stream/chat-get

Stream chat response với query parameters:

```bash
curl "http://localhost:8000/api/stream/chat-get?user_input=Hello&provider=openai"
```

### 4. **Response Format**

Tất cả streaming endpoints trả về SSE format:

```
data: {"chunk": "text chunk here", "done": false}
data: {"chunk": "more text", "done": false}
data: {"chunk": "", "done": true}
```

Nếu có lỗi:
```
data: {"error": "error message", "done": true}
```

## Cách sử dụng

### 1. Khởi động server

```bash
# Đảm bảo đã cài đặt dependencies
pip install -r requirements.txt

# Chạy server
python -m app.main
```

Server sẽ chạy tại: http://localhost:8000

### 2. Kiểm tra API Documentation

Truy cập: http://localhost:8000/docs

### 3. Test với HTML Client

Mở file `test_stream.html` trong trình duyệt để test streaming trực tiếp:

1. Chọn provider (Gemini hoặc OpenAI)
2. Nhập câu hỏi
3. Nhấn "Gửi và Stream Response"
4. Xem response được stream theo thời gian thực

### 4. Test với Python Client

```python
import requests
import json

url = "http://localhost:8000/api/stream/chat-get"
params = {
    "user_input": "Giải thích về AI",
    "provider": "gemini"
}

response = requests.get(url, params=params, stream=True)

for line in response.iter_lines():
    if line:
        line = line.decode('utf-8')
        if line.startswith('data: '):
            data = json.loads(line[6:])
            if not data.get('done'):
                print(data['chunk'], end='', flush=True)
            else:
                print("\n✅ Done!")
                break
```

### 5. Test với JavaScript (Browser)

```javascript
const eventSource = new EventSource(
    'http://localhost:8000/api/stream/chat-get?user_input=Hello&provider=gemini'
);

eventSource.onmessage = (event) => {
    const data = JSON.parse(event.data);
    
    if (data.done) {
        console.log('Stream completed!');
        eventSource.close();
    } else {
        console.log(data.chunk);
    }
};

eventSource.onerror = (error) => {
    console.error('Error:', error);
    eventSource.close();
};
```

## Cấu hình

Đảm bảo file `.env` có các API keys cần thiết:

```env
OPENAI_API_KEY=your_openai_key_here
GEMINI_API_KEY=your_gemini_key_here
```

## Lưu ý

1. **Gemini Streaming**: Sử dụng thread pool để xử lý sync API của Gemini
2. **OpenAI Streaming**: Sử dụng native async streaming của OpenAI SDK
3. **CORS**: Đã cấu hình cho phép tất cả origins (nên giới hạn trong production)
4. **Connection Keep-Alive**: Headers đã được set để maintain SSE connection

## Troubleshooting

### Server không stream response
- Kiểm tra API keys đã được cấu hình đúng chưa
- Xem logs trong console
- Test health endpoint: http://localhost:8000/health

### Client không nhận được chunks
- Đảm bảo sử dụng `stream=True` khi request với Python
- Với JavaScript, dùng `EventSource` API
- Kiểm tra CORS settings nếu gọi từ domain khác

### Response bị delay
- Đây là behavior bình thường của streaming
- Gemini có thể có độ trễ cao hơn OpenAI
- Network latency cũng ảnh hưởng đến streaming speed

## API Examples

### Demo SSE Endpoint
```bash
curl http://localhost:8000/api/stream/sse
```

### Health Check
```bash
curl http://localhost:8000/health
```

### Non-streaming Chat (Original)
```bash
curl -X POST http://localhost:8000/api/flows/ask \
  -H "Content-Type: application/json" \
  -d '{"user_input": "Hello"}'
```

## Kết luận

Bạn đã có đầy đủ các công cụ để:
- ✅ Stream responses từ Gemini
- ✅ Stream responses từ OpenAI GPT
- ✅ Tạo custom streaming flows
- ✅ Test streaming với HTML client
- ✅ Integrate streaming vào ứng dụng của bạn

Happy coding! 🎉

