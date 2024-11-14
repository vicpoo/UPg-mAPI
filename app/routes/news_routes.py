from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models.news import News
from app.schemas.news_schema import NewsCreate, NewsResponse
from app.shared.config.db import get_db

newsRoutes = APIRouter()

@newsRoutes.post('/news/', response_model=NewsResponse, status_code=status.HTTP_201_CREATED)
async def create_news(news: NewsCreate, db: Session = Depends(get_db)):
    """Create a new news item."""
    db_news = News(**news.dict())
    db.add(db_news)
    db.commit()
    db.refresh(db_news)
    return db_news

@newsRoutes.get('/news/', response_model=List[NewsResponse])
async def get_news(db: Session = Depends(get_db)):
    """Retrieve all news items."""
    news = db.query(News).all()
    return news

@newsRoutes.put('/news/{news_id}', response_model=NewsResponse)
async def update_news(news_id: int, news: NewsCreate, db: Session = Depends(get_db)):
    """Update a news item by ID."""
    db_news = db.query(News).filter(News.id == news_id).first()
    if db_news is None:
        raise HTTPException(status_code=404, detail="News not found")
    for key, value in news.dict().items():
        setattr(db_news, key, value)
    db.commit()
    db.refresh(db_news)
    return db_news

@newsRoutes.delete('/news/{news_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_news(news_id: int, db: Session = Depends(get_db)):
    """Delete a news item by ID."""
    db_news = db.query(News).filter(News.id == news_id).first()
    if db_news is None:
        raise HTTPException(status_code=404, detail="News not found")
    db.delete(db_news)
    db.commit()
    return {"message": "News deleted"}
