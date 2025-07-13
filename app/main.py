from fastapi import FastAPI, Depends
from .routers import example_router  # 예시 라우터, 실제 라우터로 교체 필요
from .core.database import engine, SessionLocal
import uuid
import datetime
from app.models.NewsArticle import NewsArticle
from app.models.source import Source
from app.models.history import History
from app.models.keyword import UserKeyword
from app.models.preferred_source import UserPreferredSource
from app.models.token import UserToken
from app.models.user import User
from sqlalchemy.orm import Session
from app.core.database import Base
from app.test.create_test_data import create_test_data

app = FastAPI()

# 라우터 등록 (예시)
app.include_router(example_router.router)

# Create tables
Base.metadata.create_all(bind=engine)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root():
    return {"message": "News Briefing Backend is running."} 


@app.get("/articles")
def read_articles(db: Session = Depends(get_db)):
    return db.query(NewsArticle).all()

@app.get("/test")
def create_Test_data():
    create_test_data()
    return {"message": "테스트 데이터 생성 완료"} 
