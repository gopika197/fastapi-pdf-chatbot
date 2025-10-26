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

# ---------------- PDF Utilities ---------------- #
def extract_pdf_text(file_bytes: bytes) -> str:
    reader = PdfReader(file_bytes)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text.strip()


def chunk_text(text: str, chunk_size: int = 3000, overlap: int = 200):
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks


@router.get("/upload")
def upload_page(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})

@router.post("/answer")
async def answer(
    request: Request,
    file: UploadFile,
    question: str = Form(...)
):
    # Get JWT from cookie
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Unauthorized")

    # Validate PDF
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are accepted")

    # Read PDF content
    content = await file.read()
    text = extract_text_from_pdf(content)
    if not text:
        raise HTTPException(status_code=400, detail="Empty PDF or couldn't extract text")

    # caching key
    key = f"{hash(content)}::{question}"

    def compute():
        return ask_llm(text, question)

    # get answer from cache or compute
    answer_text = cache_get_or_set(key, compute, ttl_seconds=300)

    return {"answer": answer_text}
# @router.post("/answer")
# def answer(request: Request, file: bytes = Form(...), question: str = Form(...)):
#     # Validate JWT from cookie
#     token = request.cookies.get("access_token")
#     if not token:
#         raise HTTPException(status_code=401, detail="Unauthorized")

#     # Extract text from PDF (implement your extract_text_from_pdf function)
#     text = extract_text_from_pdf(file)
#     if not text:
#         raise HTTPException(status_code=400, detail="Empty PDF or invalid file")

#     answer = ask_llm(text, question)
#     return {"answer": answer}