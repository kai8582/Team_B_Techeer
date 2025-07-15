from fastapi import APIRouter, Depends, HTTPException, status, Request, Response
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.user import create_user, get_user_by_email, login_process
from app.models.user import User
from app.utils.jwt_utils import create_access_token, create_refresh_token, verify_token
from app.schemas.user import (
    UserCreate, UserResponse, UserLogin,
    TokenRefresh, TokenResponse, RegisterResponse
)
import logging
from datetime import datetime

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=RegisterResponse)  # 회원가입
async def register_user(user_data: UserCreate, db: Session = Depends(get_db)):
    request_user = get_user_by_email(db, user_data.email)

    if request_user is None:
        user = create_user(db, user_data.email, user_data.password)
        return RegisterResponse(message="회원가입이 완료되었습니다.", email=user_data.email)
    else:
        raise HTTPException(status_code=404, detail="회원가입이 실패했습니다.")


@router.post("/login", response_model=TokenResponse)  # 로그인
async def login_user(user_data: UserLogin, response: Response, db: Session = Depends(get_db)):
    user = login_process(db, user_data.email, user_data.password)

    if user is False:
        raise HTTPException(status_code=404, detail="이메일 또는 비밀번호가 올바르지 않습니다")
    
    refresh_token = create_refresh_token(user.id)
    user.refresh_token = refresh_token
    user.updated_at = datetime.now()
    db.commit()

    access_token = create_access_token(user.id)

    response.headers["Authorization"] = f"Bearer {access_token}"
    
    return TokenResponse(
        message="로그인이 완료되었습니다.",
        access_token=access_token,
        refresh_token=refresh_token
    )

@router.post("/refresh", response_model=TokenResponse)  # 토큰 갱신
async def refresh_token(token_data: TokenRefresh, response: Response, db: Session = Depends(get_db)):
    # 리프레시 토큰 검증
    payload = verify_token(token_data.refresh_token)
    if not payload:
        raise HTTPException(status_code=401, detail="유효하지 않은 리프레시 토큰입니다")
    
    # 토큰 타입 확인 (refresh 토큰인지)
    if payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="잘못된 토큰 타입입니다")
    
    # 사용자 ID 추출 및 사용자 확인
    user_id = payload.get("User_id")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="사용자를 찾을 수 없습니다")
    
    # 새로운 액세스 토큰 발급
    new_access_token = create_access_token(user.id)
    response.headers["Authorization"] = f"Bearer {new_access_token}"

    user.updated_at = datetime.now()
    db.commit()

    return TokenResponse(
        message="토큰이 성공적으로 갱신되었습니다",
        refresh_token=token_data.refresh_token,
        access_token=new_access_token
    )

# 미들웨어 테스트용 엔드포인트
@router.get("/test-middleware")
async def test_middleware(request: Request):
    """미들웨어가 제대로 작동하는지 테스트하는 엔드포인트"""
    # request.state에서 미들웨어가 설정한 정보 확인
    user_id = getattr(request.state, 'user_id', None)
    user_payload = getattr(request.state, 'user_payload', None)
    
    return {
        "message": "미들웨어 테스트 성공!",
        "user_id_from_middleware": user_id,
        "user_payload_from_middleware": user_payload,
    }