# app/models/__init__.py
from .user import User
from .news_article import NewsArticle
from .press import Press
from .user_keyword import UserKeyword
from .user_preferred_press import UserPreferredPress
from .article_history import ArticleHistory

__all__ = [
    "User",
    "NewsArticle", 
    "Press",
    "UserKeyword",
    "UserPreferredPress",
    "ArticleHistory",
]
