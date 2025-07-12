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