from celery import Celery

# Celery 앱 생성
celery_app = Celery(
    "worker",
    broker="amqp://guest:guest@rabbitmq:5672//",  # RabbitMQ 브로커
    backend="redis://redis:6379/0"                # Redis 결과 저장소
)

# 간단한 덧셈 태스크 정의
@celery_app.task
def add(x, y):
    return x + y