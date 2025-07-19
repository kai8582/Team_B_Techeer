from fastapi import APIRouter, Depends
from app.schemas.user_setting import UserSetting
from app.models.user import User
from app.core.database import get_db
from sqlalchemy.orm import Session
from app.services.user_setting import get_user, get_user_history
from fastapi import HTTPException
from app.models.user_category import UserCategory
from app.schemas.user_setting import UserHistory, UserHistoryItem
from app.models.article_history import ArticleHistory
from app.models.news_article import NewsArticle
from app.models.category import Category
from app.models.press import Press
from app.models.user_preferred_press import UserPreferredPress
from app.models.user_keyword import UserKeyword

router = APIRouter(prefix="/user", tags=["user"])

@router.put("/press", response_model=UserSetting)
def user_press_setting(user_id: str, user_setting: UserSetting, db: Session = Depends(get_db)):
    user = get_user(user_id, db)

    if user is None: 
        raise HTTPException(status_code=404, detail="User not found")
    
    if user_setting.press is not None:
        # 기존 언론사 관계 삭제 (있을 경우에만)
        existing_press = db.query(UserPreferredPress).filter(UserPreferredPress.user_id == user_id).all()
        if existing_press:
            db.query(UserPreferredPress).filter(UserPreferredPress.user_id == user_id).delete()
        
        for press_name in user_setting.press:
            press = db.query(Press).filter(Press.press_name == press_name).first()
            if press:
                user_press = UserPreferredPress(
                    user_id=user_id,
                    press_id=press.id
                )
                db.add(user_press)
        
        db.commit()
        db.refresh(user)
        # 실제 선택된 언론사 이름들 가져오기
        selected_press_names = []
        for user_press in user.preferred_presses:
            press = db.query(Press).filter(Press.id == user_press.press_id).first()
            if press:
                selected_press_names.append(press.press_name)
        
        return UserSetting(
            press=selected_press_names
        )
    else:
        raise HTTPException(status_code=400, detail="Press is required")
    
@router.put("/category", response_model=UserSetting)
def user_category_setting(user_id: str, user_setting: UserSetting, db: Session = Depends(get_db)):
    user = get_user(user_id, db)

    if user is None: 
        raise HTTPException(status_code=404, detail="User not found")
    
    if user_setting.category is not None:
        # 기존 카테고리 관계 삭제 (있을 경우에만)
        existing_category = db.query(UserCategory).filter(UserCategory.user_id == user_id).all()
        if existing_category:
            db.query(UserCategory).filter(UserCategory.user_id == user_id).delete()
        
        for category_name in user_setting.category:
            category = db.query(Category).filter(Category.category_name == category_name).first()
            if category:
                user_category = UserCategory(
                    user_id=user_id,
                    category_id=category.id
                )
                db.add(user_category)
        
        db.commit()
        db.refresh(user)
        # 실제 선택된 카테고리 이름들 가져오기
        selected_category_names = []
        for user_category in user.user_categories:
            category = db.query(Category).filter(Category.id == user_category.category_id).first()
            if category:
                selected_category_names.append(category.category_name)
        
        return UserSetting(
            category=selected_category_names
        )
    else:
        raise HTTPException(status_code=400, detail="Category is required")

@router.put("/keyword", response_model=UserSetting)
def user_keyword_setting(user_id: str, user_setting: UserSetting, db: Session = Depends(get_db)):
    user = get_user(user_id, db)

    if user is None: 
        raise HTTPException(status_code=404, detail="User not found")
    
    if user_setting.keyword is not None:
        # 기존 키워드 관계 삭제 (있을 경우에만)
        existing_keyword = db.query(UserKeyword).filter(UserKeyword.user_id == user_id).all()
        if existing_keyword:
            db.query(UserKeyword).filter(UserKeyword.user_id == user_id).delete()
        
        for keyword in user_setting.keyword:
            user_keyword = UserKeyword(
                user_id=user_id,
                keyword=keyword
            )
            db.add(user_keyword)
        
        db.commit()
        db.refresh(user)
        # 실제 선택된 키워드들 가져오기
        selected_keywords = []
        for user_keyword in user.keywords:
            selected_keywords.append(user_keyword.keyword)
        
        return UserSetting(
            keyword=selected_keywords
        )
    else:
        raise HTTPException(status_code=400, detail="Keyword is required")
    
@router.get("/history", response_model=UserHistory)
def user_history(user_id: str, db: Session = Depends(get_db)):
    user = get_user(user_id, db)
    if user is None: 
        raise HTTPException(status_code=404, detail="User not found")
    
    histories = get_user_history(user_id, db)

    user_history = []
    for history in histories:
        article = history.article

        if history.news_id is None:
            raise HTTPException(status_code=404, detail="News not found")
        
        if article.thumbnail_image_url is None:
            raise HTTPException(status_code=404, detail="Thumbnail image not found")
        
        if article.url is None:
            raise HTTPException(status_code=404, detail="URL not found")
        

        user_history.append({
            "user_id": user.id,
            "news_id": history.news_id,
            "title": article.title,
            "thumbnail_image_url": article.thumbnail_image_url,
            "url": article.url,
            "category": article.category.category_name,
            "viewed_at": history.viewed_at
        })
    
    return UserHistory(histories=user_history)