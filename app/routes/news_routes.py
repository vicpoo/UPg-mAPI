from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.news import News
from app.schemas.news_schema import NewsResponse
from app.shared.config.db import get_db
import base64
import io
from PIL import Image

newsRoutes = APIRouter()

def resize_image(image_data, max_size=(800, 800)):
    """Redimensiona la imagen para no exceder el tamaño permitido."""
    image = Image.open(io.BytesIO(image_data))
    image.thumbnail(max_size, Image.LANCZOS)  # Redimensionar usando LANCZOS
    output = io.BytesIO()
    image.save(output, format="JPEG")  # Guardar en formato JPEG
    return output.getvalue()

@newsRoutes.post('/news/', response_model=NewsResponse, status_code=status.HTTP_201_CREATED)
async def create_news(
    titulo: str = Form(...),
    contenido_completo: str = Form(...),
    resumen: str = Form(None),
    imagen: UploadFile = File(...),  # Imagen obligatoria
    db: AsyncSession = Depends(get_db)
):
    """Crear una nueva noticia con una imagen obligatoria."""
    image_data = await imagen.read()
    imagen_redimensionada = resize_image(image_data)  # Redimensionar la imagen

    nueva_noticia = News(
        titulo=titulo,
        contenido_completo=contenido_completo,
        resumen=resumen,
        imagen=imagen_redimensionada
    )
    db.add(nueva_noticia)
    await db.commit()
    await db.refresh(nueva_noticia)

    # Convertir imagen a Base64 para la respuesta
    if nueva_noticia.imagen:
        nueva_noticia.imagen = base64.b64encode(nueva_noticia.imagen).decode('utf-8')

    return nueva_noticia

@newsRoutes.get('/news/', response_model=List[NewsResponse])
async def get_news(db: AsyncSession = Depends(get_db)):
    """Obtener todas las noticias."""
    result = await db.execute(select(News))
    noticias = result.scalars().all()

    # Convertir imágenes a Base64
    for noticia in noticias:
        if noticia.imagen:
            noticia.imagen = f"data:image/jpeg;base64,{base64.b64encode(noticia.imagen).decode('utf-8')}"

    return noticias

@newsRoutes.get('/news/{news_id}', response_model=NewsResponse)
async def get_news_by_id(news_id: int, db: AsyncSession = Depends(get_db)):
    """Obtener una noticia por su ID, incluyendo la imagen como cadena Base64."""
    result = await db.execute(select(News).where(News.id == news_id))
    noticia = result.scalar_one_or_none()
    if noticia is None:
        raise HTTPException(status_code=404, detail="Noticia no encontrada")

    # Convertir imagen a Base64
    if noticia.imagen:
        noticia.imagen = f"data:image/jpeg;base64,{base64.b64encode(noticia.imagen).decode('utf-8')}"

    return noticia

@newsRoutes.put('/news/{news_id}', response_model=NewsResponse)
async def update_news(
    news_id: int,
    titulo: str = Form(...),
    contenido_completo: str = Form(...),
    resumen: str = Form(None),
    imagen: UploadFile = File(None),  # Imagen opcional
    db: AsyncSession = Depends(get_db)
):
    """Actualizar una noticia existente por su ID con opción de subir una nueva imagen."""
    result = await db.execute(select(News).where(News.id == news_id))
    db_noticia = result.scalar_one_or_none()
    if db_noticia is None:
        raise HTTPException(status_code=404, detail="Noticia no encontrada")

    db_noticia.titulo = titulo
    db_noticia.contenido_completo = contenido_completo
    db_noticia.resumen = resumen

    if imagen:
        image_data = await imagen.read()
        db_noticia.imagen = resize_image(image_data)

    await db.commit()
    await db.refresh(db_noticia)

    # Convertir imagen a Base64
    if db_noticia.imagen:
        db_noticia.imagen = f"data:image/jpeg;base64,{base64.b64encode(db_noticia.imagen).decode('utf-8')}"

    return db_noticia

@newsRoutes.delete('/news/{news_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_news(news_id: int, db: AsyncSession = Depends(get_db)):
    """Eliminar una noticia por su ID."""
    result = await db.execute(select(News).where(News.id == news_id))
    db_noticia = result.scalar_one_or_none()
    if db_noticia is None:
        raise HTTPException(status_code=404, detail="Noticia no encontrada")

    await db.delete(db_noticia)
    await db.commit()
    return {"message": "Noticia eliminada"}
