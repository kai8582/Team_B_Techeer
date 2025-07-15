from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    user_id: UUID
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: str
    password: str

class TokenBase(BaseModel):
    pass

class TokenRefresh(TokenBase):
    refresh_token: str

class TokenResponse(TokenBase):
    message: str
    access_token: str
    refresh_token: str
    
class RegisterResponse(BaseModel):
    email: str
    