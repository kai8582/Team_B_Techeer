from fastapi import FastAPI
from .routers import example_router  # 예시 라우터, 실제 라우터로 교체 필요

app = FastAPI()

# 라우터 등록 (예시)
app.include_router(example_router.router)

@app.get("/")
def root():
    return {"message": "News Briefing Backend is running."} 