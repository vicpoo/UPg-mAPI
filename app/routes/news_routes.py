from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models.news import News
from app.schemas.news_schema import NewsCreate, NewsResponse
from app.shared.config.db import get_db
from typing import List 

newsRoutes = APIRouter()

# Crear una noticia
@newsRoutes.post('/news/', response_model=NewsResponse, status_code=status.HTTP_201_CREATED)
async def create_news(news: NewsCreate, db: Session = Depends(get_db)):
    db_news = News(**news.dict())
    db.add(db_news)
    db.commit()
    db.refresh(db_news)
    return db_news

# Obtener todas las noticias
@newsRoutes.get('/news/', response_model=List[NewsResponse])
async def get_news(db: Session = Depends(get_db)):
    news = db.query(News).all()
    return news
