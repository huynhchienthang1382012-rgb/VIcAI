# VicAI - AI Chat Assistant Full-Stack

Hệ thống trợ lý AI đa lĩnh vực, tách riêng frontend/backend, có memory, RAG, tool calling, streaming và nhiều chế độ trả lời.

## 1) Công nghệ sử dụng

### Backend
- FastAPI (REST API + SSE streaming)
- SQLAlchemy + SQLite (lưu user, conversation, message)
- OpenAI API (LLM + embeddings)
- Kiến trúc service module: Guardrails, Memory, RAG, Prompt Router, Tool Calling

### Frontend
- React + Vite
- Markdown render (`react-markdown`)
- Giao diện 2 cột: sidebar lịch sử + khu vực hội thoại
- Dark/light mode, trạng thái đang xử lý, auth cơ bản

## 2) Cấu trúc thư mục

```txt
.
├── backend
│   ├── app
│   │   ├── api/routes        # auth, conversation, chat stream, upload files
│   │   ├── core              # config, security
│   │   ├── db                # models + DB session
│   │   ├── schemas           # pydantic models
│   │   ├── services          # llm, rag, memory, guardrails, tools, prompt router
│   │   ├── data/knowledge    # tài liệu riêng cho RAG
│   │   └── main.py
│   ├── requirements.txt
│   └── .env.example
└── frontend
    ├── src
    │   ├── components        # Sidebar, Composer, MessageBubble
    │   ├── pages/App.jsx
    │   ├── services/api.js
    │   └── styles/app.css
    ├── package.json
    └── vite.config.js
```

## 3) Chạy dự án từng bước

## Backend
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# mở .env và thêm OPENAI_API_KEY
uvicorn app.main:app --reload --port 8000
```

## Frontend
```bash
cd frontend
npm install
npm run dev
```

Mặc định frontend ở `http://localhost:5173`, backend ở `http://localhost:8000`.

## 4) Năng lực hệ thống đã có

- **Hội thoại dài + memory**: lưu message và gọi lại ngữ cảnh gần nhất.
- **RAG**: nạp knowledge base từ `backend/app/data/knowledge/*.md`, embeddings + semantic retrieval.
- **Tool calling**: calculator + current_time (mẫu để mở rộng tool thật).
- **Streaming response**: backend SSE token-by-token.
- **Prompt routing theo mode**:
  - normal / deep / fast / teach / code / summary.
- **Guardrails**: chặn một số yêu cầu nguy hiểm và input quá dài.
- **Upload file/image**: endpoint upload sẵn để mở rộng OCR/vision.

## 5) Gợi ý nâng cấp tiến gần AI cao cấp

1. Bổ sung hàng đợi tác vụ (Celery/Redis) cho tác vụ nặng (OCR, speech-to-text).
2. Thêm vector DB chuyên dụng (Qdrant/Weaviate/Pinecone) thay in-memory index.
3. Cải thiện memory thành dạng hybrid:
   - short-term memory theo conversation
   - long-term memory theo user profile và semantic memory
4. Nâng cấp tool calling sang schema chuẩn JSON + planner (ReAct / function-calling workflow).
5. Bổ sung đánh giá chất lượng tự động (hallucination checks, citation checks, regression tests).
6. Tăng bảo mật: refresh token, RBAC, rate limit, audit logs.
7. Tích hợp ASR/TTS để hỗ trợ voice assistant toàn diện.
8. Thêm observability: OpenTelemetry, tracing theo từng request/tool/model.

## 6) Giới hạn hiện tại

- Vision/audio mới ở mức scaffold (đã có upload API, chưa có pipeline OCR/STT/TTS đầy đủ).
- RAG hiện dùng nạp cục bộ khi startup; chưa có incremental indexing dashboard.
- Tool set mẫu còn ít, nhưng đã có kiến trúc để cắm thêm dễ dàng.
