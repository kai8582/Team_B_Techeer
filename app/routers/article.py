
from fastapi import APIRouter, HTTPException
from uuid import UUID
from app.core.database import SessionLocal
from app.services.article_service.query import get_article_by_id

router = APIRouter(prefix="/articles",tags=["Articles"])

@router.get("/main")
def get_articles():
    return {"message":"hello world"}

#뉴스 상세 조회 
@router.get("/{article_id}")
async def get_article_detail(article_id: UUID):
    db = SessionLocal()
    try:
        article = get_article_by_id(db, article_id)
        if not article:
            raise HTTPException(status_code=404, detail="기사를 찾을 수 없습니다.")
        article_dict = {
            "id": str(article.id),
            "title": article.title,
            "url": article.url,
            "summary_text": getattr(article, "summary_text", None),
            "categories": getattr(article, "categories", None),
            "image_url": getattr(article, "image_url", None),
            "author": getattr(article, "author", None),
            "content": getattr(article, "content", None),
        }
        try:
            article_dict["published_at"] = article.published_at.isoformat() if getattr(article, "published_at", None) else None
        except:
            article_dict["published_at"] = None
        try:
            article_dict["created_at"] = article.created_at.isoformat() if getattr(article, "created_at", None) else None
        except:
            article_dict["created_at"] = None
        return {"success": True, "article": article_dict}
    finally:
        db.close()