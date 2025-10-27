# FastAPI PDF Chatbot

## Overview
A FastAPI backend that allows users to sign up/login (JWT), upload a PDF and ask questions about its contents.
The backend extracts text from the PDF and forwards the context + question to a free LLM (Hugging Face Inference API).
This scaffold includes:
- JWT authentication (PyJWT)
- PDF parsing (PyPDF2)
- LLM integration (Hugging Face Inference API)
- Simple SQLite user store (SQLAlchemy)
- Caching (in-memory with TTL)
- Dockerfile
🚀 Features

✅ Upload and process PDF files
✅ Extract and store embeddings in FAISS vector store
✅ Query the document content with natural language
✅ Stream responses using an LLM (Hugging Face)
✅ Modular and scalable backend with FastAPI

Project Structure 
fastapi-pdf-chatbot/
│
├── app/
│   ├── main.py                 # FastAPI entry point
│   ├── routes/
│   │   └── chat.py             # Chat and upload endpoints
│   ├── core/
│   │   ├── config.py           # Environment configurations
│   │   ├── llm_service.py      # sak_llm() and LLM interaction logic
│   │   └── pdf_service.py      # PDF parsing and embedding logic
│   ├── utils/
│   │   └── vector_store.py     # FAISS vector database logic
│   ├── models/
│   │   └── schemas.py          # Pydantic models for requests/responses
│   └── __init__.py
│
├── data/
│   └── uploads/                # Folder to store uploaded PDFs
│
├── requirements.txt
└── README.md

⚙️ Installation
1️⃣ Clone the repository
git clone https://github.com/yourusername/fastapi-pdf-chatbot.git
cd fastapi-pdf-chatbot

1. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. Set environment variables (create a `.env` file):
   ```
   SECRET_KEY=your_secret_key_here
   HF_API_KEY=your_hf_api_key_here
   ```

3. Run the app:
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

4. Open docs at `http://localhost:8000/docs`.

## Endpoints
- POST /auth/signup
- POST /auth/login
- POST /chat/answer  (multipart/form-data: file (pdf), question (text)) — requires Authorization: Bearer <token>

## Notes
- This project uses the Hugging Face Inference API; you can use a free-tier HF account and models.
- For production, make sure to use HTTPS and a persistent DB.

🧩 LLM API — Hugging Face Inference API

This project uses the Hugging Face Inference API for text-based reasoning over extracted PDF content.
Model chosen: Falcon-7B-Instruct

🧠 Why Falcon-7B-Instruct?

Open-weight model with strong reasoning and summarization ability.

Fast inference via Hugging Face Inference endpoint.

Supports context-driven Q&A, suitable for summarizing PDFs and answering domain-specific questions.

🧠 Endpoints Overview
🧍 Authentication Routes
1. Signup

POST /user/signup

Request (Form data):
{
  "email": "user@example.com",
  "password": "mypassword"
}

2. Login

POST /user/login
{
  "email": "user@example.com",
  "password": "mypassword"
}

📂 File Upload & Chat Routes
3. Ask a Question

POST /chat/answer

Request (Form data):
| Field      | Type   | Description                  |
| ---------- | ------ | ---------------------------- |
| `file`     | File   | The PDF file to analyze      |
| `question` | String | The question you want to ask |

