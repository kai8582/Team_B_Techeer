<<<<<<< HEAD
from fastapi import FastAPI, Depends
from .routers import example_router  # 예시 라우터, 실제 라우터로 교체 필요
from .core.database import engine, SessionLocal
from .models.NewsArticle import NewsArticle
from sqlalchemy.orm import Session
from app.core.database import Base

app = FastAPI()

# 라우터 등록 (예시)
app.include_router(example_router.router)

# Create tables
=======
from fastapi import FastAPI
from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine, Base
from app.models.news_article import NewsArticle
from app.models.press import Press
from uuid import uuid4
from datetime import datetime

from app.models.user import User
from app.models.article_history import ArticleHistory
from app.models.news_article import NewsArticle
from app.models.press import Press
from app.models.refresh_token import RefreshToken
from app.models.user_keyword import UserKeyword
from app.models.user_preferred_press import UserPreferredPress
from uuid import uuid4
from datetime import datetime

app = FastAPI()

>>>>>>> 9770354 (feat: 초기 FastAPI + Docker + DB 세팅 완료)
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

<<<<<<< HEAD

@app.get("/articles")
def read_articles(db: Session = Depends(get_db)):
    return db.query(NewsArticle).all()




@app.on_event("startup")
def load_test_data():
    db = SessionLocal()
    if not db.query(NewsArticle).first():
        db.add_all([
            NewsArticle(title="Hello World", content="This is your first article."),
            NewsArticle(title="FastAPI Rocks", content="FastAPI is a modern web framework for Python.")
        ])
        db.commit()
    db.close()
=======
@app.on_event("startup")
def load_test_data():
    db: Session = SessionLocal()

    if not db.query(Press).first():
        press_id = str(uuid4())
        press = Press(
            id=press_id,
            press_name="한겨레",
            created_at=datetime.utcnow(),
            updated_at=None,
            is_deleted=False,
        )
        db.add(press)
        db.commit()

        article = NewsArticle(
            id=str(uuid4()),
            title="테스트 뉴스입니다",
            url="https://example.com/news/1",
            published_at=datetime.utcnow(),
            summary_text="요약 내용입니다",
            male_audio_url="https://example.com/audio/male.mp3",
            female_audio_url="https://example.com/audio/female.mp3",
            categories="IT",
            image_url="https://example.com/image.jpg",
            author="홍길동",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            is_deleted=False,
            press_id=press.id
        )
        db.add(article)
        db.commit()

    db.close()
>>>>>>> 9770354 (feat: 초기 FastAPI + Docker + DB 세팅 완료)
