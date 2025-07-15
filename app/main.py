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
        for name in press_names:
            press = Press(press_name=name)
            db.add(press)
        db.commit()

    # 크롤링 예시
    crawling_result = {
        "press_name": "SBS",
        "title": "테스트 뉴스입니다",
        "url": "https://example.com/news/1",
        "published_at": datetime(2025, 7, 10, 8, 0),
        "summary_text": "요약 내용입니다",
        "categories": "IT",
        "author": "홍길동",
    }

    # 언론사 이름으로 press.id 가져오기
    press = db.query(Press).filter_by(press_name=crawling_result["press_name"]).first()

    if press is None:
        print(f"'{crawling_result['press_name']}' 언론사는 presses 테이블에 존재하지 않습니다.")
        db.close()
        return 


    article = NewsArticle(
        title=crawling_result["title"],
        url=crawling_result["url"],
        published_at=crawling_result["published_at"],
        summary_text=crawling_result["summary_text"],
        categories=crawling_result["categories"],
        author=crawling_result["author"],
        press_id=press.id
    )
    db.add(article)
    db.commit()
    db.close()