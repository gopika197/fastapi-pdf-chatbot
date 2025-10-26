# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from app.routes.user_routes import router as user_router
# from app.routes.chat_routes import router as chat_router

# app = FastAPI(title="PDF Chatbot API")

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# app.include_router(user_router, prefix="/auth", tags=["Authentication"])
# app.include_router(chat_router, prefix="/chat", tags=["Chat"])



# @app.get("/")
# def root():
#     return {"message": "PDF Chatbot API. See /docs for OpenAPI."}
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from app.routes.user_routes import router as user_router
from app.routes.chat_routes import router as chat_router
from fastapi.templating import Jinja2Templates
import os

app = FastAPI()
app.include_router(user_router, prefix="/user")  # /user/login and /user/signup
app.include_router(chat_router, prefix="/chat")

# Templates
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# Static files
static_dir = os.path.join(BASE_DIR, "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")
else:
    print(f"Warning: static directory '{static_dir}' does not exist. Skipping mounting static files.")

# Root redirects to login page
@app.get("/", include_in_schema=False)
def home():
    return RedirectResponse("/user/login")
