from sqlalchemy import Column, Boolean, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import Base
from datetime import datetime
import uuid


class UserPreferredPress(Base):
    __tablename__ = "user_preferred_presses"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime)
    is_deleted = Column(Boolean, nullable=False, default=False)

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    press_id = Column(UUID(as_uuid=True), ForeignKey("presses.id"), nullable=False)

    user = relationship("User", back_populates="preferred_presses")
    press = relationship("Press", back_populates="preferred_by")