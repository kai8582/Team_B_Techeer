from sqlalchemy import Column, Boolean, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base
from datetime import datetime
import uuid

class PressCategory(Base):
    __tablename__ = "presses_categroies"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_deleted = Column(Boolean, nullable=False, default=False)
    
    cateogry_id = Column(UUID(as_uuid=True), ForeignKey("categories.id"), nullable=False)
    press_id = Column(UUID(as_uuid=True), ForeignKey("presses.id"), nullable=False)
    
    category = relationship("Category", back_populates="press_categories")
    press = relationship("Press", back_populates="press_categories")
