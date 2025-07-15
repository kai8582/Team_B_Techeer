from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from app.utils.jwt_utils import verify_token
import logging

logger = logging.getLogger(__name__)

class AuthMiddleware(BaseHTTPMiddleware):
    """JWT 토큰 인증을 위한 미들웨어"""
    
    def __init__(self, app, public_paths=None):
        super().__init__(app)
        # 인증이 필요하지 않은 공개 경로들
        self.public_paths = public_paths or [
            "/",
            "/docs",
            "/redoc", 
            "/openapi.json",
            "/health",
            "/api/v1/auth/login",
            "/api/v1/auth/register",
            "/api/v1/auth/refresh"
        ]
    
    async def dispatch(self, request: Request, call_next):
        logger.info(f"Middleware processing: {request.url.path}")
        
        # 현재 경로가 공개 경로인지 확인 (정확한 매칭)
        is_public_path = request.url.path in self.public_paths
        
        if is_public_path:
            # 공개 경로는 인증 없이 통과
            logger.info(f"Public path, skipping auth: {request.url.path}")
            return await call_next(request)
        
        # Authorization 헤더 확인
        auth_header = request.headers.get("Authorization")
        logger.info(f"Auth header: {auth_header[:50] if auth_header else 'None'}...")
        
        if not auth_header or not auth_header.startswith("Bearer "): # 토큰이 없으면 401 에러
            logger.info("No valid Authorization header found")
            return JSONResponse(
                content='{"detail": "Authorization header is required"}',
                status_code=401,
            )
        
        # 토큰 추출
        token = auth_header.split(" ")[1]
        
        # 토큰 검증
        payload = verify_token(token)
        logger.info(f"Token verification result: {payload}")
        
        if not payload: # 토큰 검증
            logger.info("Token verification failed")
            return JSONResponse(
                content='{"detail": "Invalid or expired token"}',
                status_code=401
            )
            
        # 토큰 타입 확인 (access 토큰인지)
        if payload.get("type") != "access":
            return JSONResponse(
                content='{"detail": "Invalid token type"}',
                status_code=401
            )
            
        # 요청에 사용자 정보 추가 (User_id 사용)
        user_id = payload.get("User_id")  # User_id에서 UUID 문자열 가져오기
        logger.info(f"Setting user_id in request.state: {user_id}")
        
        request.state.user_id = user_id
        request.state.user_payload = payload
                        
        return await call_next(request) 