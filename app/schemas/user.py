from pydantic import BaseModel

class UserBase(BaseModel):
    email: str
    password: str

class RegisterResponse(BaseModel):
    message: str
    email: str
    access_token: str
    refresh_token: str

class LoginResponse(BaseModel):
    message: str
    access_token: str
    refresh_token: str

class RefreshRequest(BaseModel):
    refresh_token: str