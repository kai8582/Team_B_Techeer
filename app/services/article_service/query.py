from typing import List
import uuid
from dotenv.main import logger
from sqlalchemy.orm import Session
from app.models.news_article import NewsArticle
from app.models.press import Press


def get_recent_articles(db: Session, limit: int = 20) -> List[NewsArticle]:
    """
    최근 기사 조회
    
    Args:
        db: 데이터베이스 세션
        limit: 조회할 기사 수
    Returns:
        NewsArticle 객체 리스트
    """
    return db.query(NewsArticle).filter(
        NewsArticle.is_deleted == False
    ).order_by(NewsArticle.published_at.desc()).limit(limit).all()

def get_articles_by_press(db: Session, press_name: str, limit: int = 10) -> List[NewsArticle]:
    """
    언론사별 기사 조회
    
    Args:
        db: 데이터베이스 세션
        press_name: 언론사명
        limit: 조회할 기사 수
    
    Returns:
        NewsArticle 객체 리스트
    """
    return db.query(NewsArticle).join(Press).filter(
        Press.press_name == press_name,
        NewsArticle.is_deleted == False
    ).order_by(NewsArticle.published_at.desc()).limit(limit).all()

def delete_article(db: Session, article_id: str) -> bool:
    """
    기사 삭제 (소프트 삭제)
    
    Args:
        db: 데이터베이스 세션
        article_id: 기사 ID
    
    Returns:
        삭제 성공 여부
    """
    try:
        article = db.query(NewsArticle).filter(
            NewsArticle.id == uuid.UUID(article_id),
            NewsArticle.is_deleted == False
        ).first()
        
        if article:
            article.is_deleted = True
            db.commit()
            logger.info(f"기사 삭제 완료: {article_id}")
            return True
        else:
            logger.warning(f"삭제할 기사를 찾을 수 없음: {article_id}")
            return False
            
    except Exception as e:
        logger.error(f"기사 삭제 실패: {e}")
        db.rollback()
        return False 

def get_articles_by_category(db: Session, category: str, limit: int = 10) -> List[NewsArticle]:
    """
    카테고리별 기사 조회
    
    Args:
        db: 데이터베이스 세션
        category: 카테고리명
        limit: 조회할 기사 수
    
    Returns:
        NewsArticle 객체 리스트
    """
    return db.query(NewsArticle).filter(
        NewsArticle.categories == category,
        NewsArticle.is_deleted == False
    ).order_by(NewsArticle.published_at.desc()).limit(limit).all()