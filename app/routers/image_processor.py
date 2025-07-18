from fastapi import APIRouter, HTTPException, Depends
from app.services.article_service.query import get_article_by_id
from app.services.article_service.image_process import process_image_to_s3
from app.core.database import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/image", tags=["image"])

@router.post("/process")
async def process_image_endpoint(article_id: str, db: Session = Depends(get_db)):
    try:
        # 기사 존재 확인
        article = get_article_by_id(db, article_id)
        if not article:
            raise HTTPException(status_code=404, detail="기사를 찾을 수 없습니다")
        
        # 이미지 URL 확인
        if not article.original_image_url:
            raise HTTPException(status_code=400, detail="기사에 이미지 URL이 없습니다")
        
        # 이미지 처리 및 S3 업로드
        result = process_image_to_s3(db, article_id)
        
        if result["success"]:
            return {
                "message": "이미지 처리 및 S3 업로드 완료",
                "article_id": article_id,
                "thumbnail_url": result["s3_urls"]["thumbnail"],
                "original_url": result["original_url"]
            }
        else:
            raise HTTPException(status_code=500, detail=f"이미지 처리 실패: {result.get('error', '알 수 없는 오류')}")
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"서버 오류: {str(e)}")