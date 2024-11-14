from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.news import News
from app.schemas.news_schema import NewsCreate, NewsResponse
from app.shared.config.db import get_db

newsRoutes = APIRouter()

@newsRoutes.post('/news/', response_model=NewsResponse, status_code=status.HTTP_201_CREATED)
async def create_news(news: NewsCreate, db: AsyncSession = Depends(get_db)):
    """Create a new news item."""
    db_news = News(**news.dict())
    db.add(db_news)
    await db.commit()
    await db.refresh(db_news)
    return db_news

@newsRoutes.get('/news/', response_model=List[NewsResponse])
async def get_news(db: AsyncSession = Depends(get_db)):
    """Retrieve all news items."""
    result = await db.execute(select(News))
    news = result.scalars().all()
    return news

@newsRoutes.put('/news/{news_id}', response_model=NewsResponse)
async def update_news(news_id: int, news: NewsCreate, db: AsyncSession = Depends(get_db)):
    """Update a news item by ID."""
    result = await db.execute(select(News).filter(News.id == news_id))
    db_news = result.scalar_one_or_none()
    if db_news is None:
        raise HTTPException(status_code=404, detail="News not found")
    for key, value in news.dict().items():
        setattr(db_news, key, value)
    await db.commit()
    await db.refresh(db_news)
    return db_news

@newsRoutes.delete('/news/{news_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_news(news_id: int, db: AsyncSession = Depends(get_db)):
    """Delete a news item by ID."""
    result = await db.execute(select(News).filter(News.id == news_id))
    db_news = result.scalar_one_or_none()
    if db_news is None:
        raise HTTPException(status_code=404, detail="News not found")
    await db.delete(db_news)
    await db.commit()
    return {"message": "News deleted"}
