from fastapi import APIRouter, Request, Form, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from app.services.user_service import UserService
from app.utils.jwt_utils import create_access_token
import os

router = APIRouter()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "../templates"))

# Signup page GET
@router.get("/signup")
def signup_page(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

# Signup POST
@router.post("/signup")
def signup(request: Request, email: str = Form(...), password: str = Form(...)):
    created = UserService.create_user(email, password)
    if not created:
        return templates.TemplateResponse("signup.html", {"request": request, "error": "User already exists"})
    return RedirectResponse("/user/login", status_code=status.HTTP_302_FOUND)

# Login page GET
@router.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

# Login POST
@router.post("/login")
def login(request: Request, email: str = Form(...), password: str = Form(...)):
    
    user = UserService.authenticate(email, password)
    print("Login success for:", user,email, password)
    if not user:
        print("not user")
        return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid credentials"})
    
    token = create_access_token({"sub": user.email})
    response = RedirectResponse(url="/user/upload", status_code=status.HTTP_302_FOUND)
    response.set_cookie(key="access_token", value=token, httponly=True)
    return response

# Upload page GET
@router.get("/upload")
def upload_page(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})
