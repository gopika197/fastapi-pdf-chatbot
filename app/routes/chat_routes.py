from fastapi import APIRouter, File, Form, UploadFile, Depends, HTTPException, status, Request
from fastapi.responses import RedirectResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.utils.pdf_utils import extract_text_from_pdf
from app.utils.jwt_utils import verify_token
from app.utils.llm_utils import ask_llm
from app.services.cache_service import cache_get_or_set
from fastapi.templating import Jinja2Templates
import os

router = APIRouter()
router = APIRouter()
security = HTTPBearer()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "../templates"))

@router.get("/upload")
def upload_page(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})

@router.post("/answer")
def answer(request: Request, file: bytes = Form(...), question: str = Form(...)):
    # Validate JWT from cookie
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Unauthorized")

    # Extract text from PDF (implement your extract_text_from_pdf function)
    text = extract_text_from_pdf(file)
    if not text:
        raise HTTPException(status_code=400, detail="Empty PDF or invalid file")

    answer = ask_llm(text, question)
    return {"answer": answer}