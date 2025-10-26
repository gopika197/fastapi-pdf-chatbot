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

## Quick start (local)
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
