from fastapi import FastAPI
from sqlalchemy.orm import Session
from app.core.database import SessionLocal, engine, Base

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

@app.on_event("startup")
def load_test_data():
    db: Session = SessionLocal()

    if not db.query(Press).first():
        press_names = ["SBS", "JTBC", "한국경제"]
        presses = []
        for name in press_names:
            press = Press(
                id=str(uuid4()),
                press_name=name,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
                is_deleted=False
            )
            presses.append(press)

        db.add_all(presses)
        db.commit()

        # 첫 번째 언론사에 테스트 기사 하나 생성 (예시)
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
            press_id=presses[0].id  # SBS에 연결
        )
        db.add(article)
        db.commit()

    db.close()