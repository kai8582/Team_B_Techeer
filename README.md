# News Briefing Backend

FastAPI 기반 뉴스 브리핑 백엔드 프로젝트입니다.

## 프로젝트 구조

```
news_briefing_backend/
├── app/
│   ├── __init__.py
│   ├── main.py                # 진입점
│   ├── models/                # SQLAlchemy 모델
│   ├── routers/               # API 라우터
│   ├── services/              # GPT, TTS 등 로직
│   ├── schemas/               # Pydantic 정의
│   ├── core/                  # 설정, DB 연결 등
│   └── utils/                 # 크롤러, 알림 유틸 등
├── tests/                     # pytest 유닛테스트
├── .env
├── requirements.txt
├── Dockerfile
└── README.md
```

## 실행 방법

1. 의존성 설치

```bash
pip install -r requirements.txt
```

2. 서버 실행

```bash
uvicorn app.main:app --reload
```

## 주요 의존성
- fastapi
- uvicorn[standard]
- sqlalchemy
- pydantic
- python-dotenv 


## .env 설정
```
DB_USER=
DB_PASSWORD=
DB_NAME=
DB_URL=
```
