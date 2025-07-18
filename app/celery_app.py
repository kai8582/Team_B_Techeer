from celery import Celery
import time
from app.services.article_service.image_process import process_image_to_s3
from app.core.database import get_db
from typing import Dict

# Celery 앱 생성
celery_app = Celery(
    "worker",
    broker="amqp://guest:guest@rabbitmq:5672//",  # RabbitMQ 브로커
    backend="redis://redis:6379/0"                # Redis 결과 저장소
)

# 간단한 덧셈 태스크 정의
@celery_app.task
def add(x, y):
    time.sleep(5) # 테스트를 위해 5초 걸리는 작업 추가
    return x + y

# 이미지 처리 태스크
@celery_app.task
def process_image_async(article_id: str):
    """비동기로 이미지를 처리하는 Celery 태스크"""
    try:
        # 새로운 데이터베이스 세션 생성 (Celery 워커에서 사용)
        db = next(get_db())
        
        result = process_image_to_s3(db, article_id)
        
        # 세션 정리
        db.close()
        
        return result
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "article_id": article_id
        }

def process_image_to_s3_async(article_id: str) -> Dict:
    """이미지 처리를 비동기로 시작하고 태스크 ID 반환"""
    task = process_image_async.delay(article_id)
    
    return {
        "task_id": task.id,
        "status": "processing",
        "message": "이미지 처리가 시작되었습니다. 백그라운드에서 처리 중입니다."
    }