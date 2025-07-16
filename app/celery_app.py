from celery import Celery
import time

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