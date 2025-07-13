from sqlalchemy import Column, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.core.database import Base
import uuid
import datetime

class NewsArticle(Base):
    __tablename__ = "news_article"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(255), nullable=False)
    url = Column(String(225), nullable=False)
    published_at = Column(DateTime, nullable=False)
    summary_text = Column(Text, nullable=False)
    m_audio_url = Column(String(100), nullable=False)
    fm_audio_url = Column(String(100), nullable=False)
    categories = Column(String(20), nullable=False)
    image_url = Column(String(200), nullable=False)
    author = Column(String(20), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, nullable=True)
    is_deleted = Column(Boolean, default=False, nullable=False)

    press_id = Column(UUID(as_uuid=True), ForeignKey("sources.id"), nullable=False)