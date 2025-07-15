from fastapi import FastAPI, Depends, Request, Response
from .routers import example_router, user
from .core.database import engine, SessionLocal
from sqlalchemy.orm import Session
from app.core.database import Base
from app.models.user import User
from fastapi.middleware.cors import CORSMiddleware
# from starlette.middleware.sessions import SessionMiddleware
from app.middleware.auth_middleware import AuthMiddleware
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

origins = [
    #추가해서 사용
]   

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# SECRET_KEY = os.getenv("SECRET_KEY")
# app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)

# 인증 미들웨어 추가
app.add_middleware(AuthMiddleware)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 라우터 등록
app.include_router(example_router.router)
app.include_router(user.router, prefix="/api/v1")

# Create tables
Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "News Briefing Backend is running."} 