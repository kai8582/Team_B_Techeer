from sqlalchemy import Column, DateTime, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base
from datetime import datetime
import uuid

class ArticleHistory(Base):
    __tablename__ = 'article_histories'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    viewed_at = Column(DateTime, nullable=False)

    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_deleted = Column(Boolean, nullable=False, default=False)

    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    news_id = Column(UUID(as_uuid=True), ForeignKey('news_articles.id'), nullable=False)

    user = relationship("User", back_populates="article_histories")
    article = relationship("NewsArticle", back_populates="histories")