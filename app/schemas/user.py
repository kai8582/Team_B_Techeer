from pydantic import BaseModel

class RegisterRequest(BaseModel):
    email: str
    password: str

class RegisterResponse(BaseModel):
    message: str
    email: str

class LoginRequest(BaseModel):
    email: str
    password: str

class LoginResponse(BaseModel):
    message: str
    access_token: str
    refresh_token: str

class RefreshRequest(BaseModel):
    refresh_token: str

class RefreshResponse(BaseModel):
    message: str
    access_token: str
    refresh_token: str
    