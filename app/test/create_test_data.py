import os
import sys
import uuid
import datetime
from dotenv import load_dotenv
# .env 파일 로드
load_dotenv()

from app.core.database import SessionLocal
from app.models.user import User
from app.models.source import Source
from app.models.NewsArticle import NewsArticle
from app.models.token import UserToken
from app.models.keyword import UserKeyword
from app.models.preferred_source import UserPreferredSource
from app.models.history import History

def create_test_data():
    db = SessionLocal()
    
    try:
        print("테스트 데이터 생성 시작...")
        
        # 1. 사용자 데이터 생성
        print("1. 사용자 데이터 생성 중...")
        users = []
        for i in range(3):
            user = User(
                voice_type=f"voice_type_{i+1}",
                alarm_token=f"alarm_token_{i+1}_{uuid.uuid4().hex[:10]}",
                device_id=f"device_{i+1}_{uuid.uuid4().hex[:8]}",
                created_at=datetime.datetime.utcnow(),
                updated_at=datetime.datetime.utcnow(),
                is_deleted=False
            )
            users.append(user)
        
        db.add_all(users)
        db.commit()
        print(f"   ✅ {len(users)}명의 사용자 생성 완료")
        
        # 2. 언론사 데이터 생성
        print("2. 언론사 데이터 생성 중...")
        press_names = ["조선일보", "중앙일보", "동아일보", "한겨레", "경향신문", "서울신문"]
        sources = []
        for press_name in press_names:
            source = Source(
                press_name=press_name,
                created_at=datetime.datetime.utcnow(),
                updated_at=datetime.datetime.utcnow(),
                is_deleted=False
            )
            sources.append(source)
        
        db.add_all(sources)
        db.commit()
        print(f"   ✅ {len(sources)}개의 언론사 생성 완료")
        
        # 3. 뉴스 기사 데이터 생성
        print("3. 뉴스 기사 데이터 생성 중...")
        articles = []
        categories = ["정치", "경제", "사회", "국제", "문화", "스포츠"]
        authors = ["김기자", "이기자", "박기자", "최기자", "정기자"]
        
        for i in range(10):
            article = NewsArticle(
                title=f"테스트 뉴스 제목 {i+1} - {categories[i % len(categories)]} 관련 소식",
                url=f"https://example.com/news/{i+1}",
                published_at=datetime.datetime.utcnow() - datetime.timedelta(hours=i),
                summary_text=f"이것은 테스트 뉴스 기사 {i+1}의 요약 내용입니다. {categories[i % len(categories)]} 분야의 중요한 소식을 전해드립니다.",
                m_audio_url=f"https://audio.example.com/m/{i+1}.mp3",
                fm_audio_url=f"https://audio.example.com/fm/{i+1}.mp3",
                categories=categories[i % len(categories)],
                image_url=f"https://images.example.com/news_{i+1}.jpg",
                author=authors[i % len(authors)],
                created_at=datetime.datetime.utcnow(),
                updated_at=datetime.datetime.utcnow(),
                is_deleted=False,
                press_id=sources[i % len(sources)].id
            )
            articles.append(article)
        
        db.add_all(articles)
        db.commit()
        print(f"   ✅ {len(articles)}개의 뉴스 기사 생성 완료")
        
        # 4. 사용자 토큰 데이터 생성
        print("4. 사용자 토큰 데이터 생성 중...")
        tokens = []
        for user in users:
            token = UserToken(
                access_token=f"access_token_{user.id}_{uuid.uuid4().hex[:20]}",
                refresh_token=f"refresh_token_{user.id}_{uuid.uuid4().hex[:20]}",
                created_at=datetime.datetime.utcnow(),
                updated_at=datetime.datetime.utcnow(),
                is_deleted=False,
                user_id=user.id
            )
            tokens.append(token)
        
        db.add_all(tokens)
        db.commit()
        print(f"   ✅ {len(tokens)}개의 사용자 토큰 생성 완료")
        
        # 5. 사용자 키워드 데이터 생성
        print("5. 사용자 키워드 데이터 생성 중...")
        keywords = ["정치", "경제", "부동산", "주식", "IT", "건강", "여행", "음식"]
        user_keywords = []
        
        for user in users:
            for i in range(3):  # 각 사용자당 3개 키워드
                keyword = UserKeyword(
                    keyword=keywords[(users.index(user) * 3 + i) % len(keywords)],
                    created_at=datetime.datetime.utcnow(),
                    updated_at=datetime.datetime.utcnow(),
                    is_deleted=False,
                    user_id=user.id
                )
                user_keywords.append(keyword)
        
        db.add_all(user_keywords)
        db.commit()
        print(f"   ✅ {len(user_keywords)}개의 사용자 키워드 생성 완료")
        
        # 6. 사용자 선호 언론사 데이터 생성
        print("6. 사용자 선호 언론사 데이터 생성 중...")
        preferred_sources = []
        types = ["아침", "저녁", "전체"]
        
        for user in users:
            for i in range(2):  # 각 사용자당 2개 선호 언론사
                preferred_source = UserPreferredSource(
                    type=types[i % len(types)],
                    created_at=datetime.datetime.utcnow(),
                    updated_at=datetime.datetime.utcnow(),
                    is_deleted=False,
                    user_id=user.id,
                    press_id=sources[i % len(sources)].id
                )
                preferred_sources.append(preferred_source)
        
        db.add_all(preferred_sources)
        db.commit()
        print(f"   ✅ {len(preferred_sources)}개의 사용자 선호 언론사 생성 완료")
        
        # 7. 히스토리 데이터 생성
        print("7. 히스토리 데이터 생성 중...")
        histories = []
        
        for user in users:
            for i in range(3):  # 각 사용자당 3개 히스토리
                history = History(
                    viewed_at=datetime.datetime.utcnow() - datetime.timedelta(hours=i),
                    created_at=datetime.datetime.utcnow(),
                    updated_at=datetime.datetime.utcnow(),
                    is_deleted=False,
                    user_id=user.id,
                    news_id=articles[i % len(articles)].id
                )
                histories.append(history)
        
        db.add_all(histories)
        db.commit()
        print(f"   ✅ {len(histories)}개의 히스토리 생성 완료")
        
        print("\n🎉 모든 테스트 데이터 생성 완료!")
        print(f"   - 사용자: {len(users)}명")
        print(f"   - 언론사: {len(sources)}개")
        print(f"   - 뉴스 기사: {len(articles)}개")
        print(f"   - 사용자 토큰: {len(tokens)}개")
        print(f"   - 사용자 키워드: {len(user_keywords)}개")
        print(f"   - 선호 언론사: {len(preferred_sources)}개")
        print(f"   - 히스토리: {len(histories)}개")
    
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        db.rollback()
        import traceback
        traceback.print_exc()
    finally:
        db.close()