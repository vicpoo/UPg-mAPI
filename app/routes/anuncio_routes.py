from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.anuncio import Anuncio
from app.schemas.anuncio_schema import AnuncioResponse
from app.shared.config.db import get_db
import base64
import io
from PIL import Image
from datetime import datetime
from typing import List  # Importa List desde typing

anuncioRoutes = APIRouter()

# Función para redimensionar la imagen (opcional)
def resize_image(image_data, max_size=(800, 800)):
    """Redimensiona la imagen para no exceder el tamaño permitido."""
    image = Image.open(io.BytesIO(image_data))
    if image.mode == 'RGBA':
        image = image.convert('RGB')
    image.thumbnail(max_size, Image.LANCZOS)
    output = io.BytesIO()
    image.save(output, format="JPEG")
    return output.getvalue()

@anuncioRoutes.post('/anuncio/', response_model=AnuncioResponse, status_code=status.HTTP_201_CREATED)
async def create_anuncio(
    imagen: UploadFile = File(...),
    db: AsyncSession = Depends(get_db)
):
    """Crea un nuevo anuncio con una imagen en base64."""
    
    # Leer y redimensionar la imagen
    image_data = await imagen.read()
    image_data = resize_image(image_data)

    # Crear un nuevo anuncio
    new_anuncio = Anuncio(imagen=image_data)
    db.add(new_anuncio)
    await db.commit()

    # Cargar el anuncio para evitar problemas de serialización
    await db.refresh(new_anuncio)

    # Procesar la imagen como base64
    if new_anuncio.imagen:
        new_anuncio.imagen = base64.b64encode(new_anuncio.imagen).decode('utf-8')

    return new_anuncio


@anuncioRoutes.get('/anuncios/', response_model=List[AnuncioResponse])  # Ahora List está importado
async def get_anuncios(db: AsyncSession = Depends(get_db)):
    """Recupera todos los anuncios."""
    result = await db.execute(select(Anuncio))
    anuncios = result.scalars().all()

    # Procesar las imágenes en Base64
    for anuncio in anuncios:
        if anuncio.imagen:
            anuncio.imagen = f"data:image/jpeg;base64,{base64.b64encode(anuncio.imagen).decode('utf-8')}"

    return anuncios


@anuncioRoutes.get('/anuncio/{anuncio_id}', response_model=AnuncioResponse)
async def get_anuncio_by_id(anuncio_id: int, db: AsyncSession = Depends(get_db)):
    """Obtiene un anuncio por su ID."""
    result = await db.execute(select(Anuncio).where(Anuncio.id == anuncio_id))
    anuncio = result.scalar_one_or_none()
    if anuncio is None:
        raise HTTPException(status_code=404, detail="Anuncio no encontrado")

    if anuncio.imagen:
        anuncio.imagen = f"data:image/jpeg;base64,{base64.b64encode(anuncio.imagen).decode('utf-8')}"

    return anuncio


@anuncioRoutes.put('/anuncio/{anuncio_id}', response_model=AnuncioResponse)
async def update_anuncio(
    anuncio_id: int,
    imagen: UploadFile = File(None),
    db: AsyncSession = Depends(get_db)
):
    """Actualiza un anuncio existente por ID con una nueva imagen."""
    result = await db.execute(select(Anuncio).where(Anuncio.id == anuncio_id))
    db_anuncio = result.scalar_one_or_none()
    if db_anuncio is None:
        raise HTTPException(status_code=404, detail="Anuncio no encontrado")

    if imagen:
        db_anuncio.imagen = await imagen.read()

    await db.commit()
    await db.refresh(db_anuncio)

    if db_anuncio.imagen:
        db_anuncio.imagen = base64.b64encode(db_anuncio.imagen).decode('utf-8')

    return db_anuncio


@anuncioRoutes.delete('/anuncio/{anuncio_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_anuncio(anuncio_id: int, db: AsyncSession = Depends(get_db)):
    """Elimina un anuncio por ID."""
    result = await db.execute(select(Anuncio).where(Anuncio.id == anuncio_id))
    db_anuncio = result.scalar_one_or_none()
    if db_anuncio is None:
        raise HTTPException(status_code=404, detail="Anuncio no encontrado")
    
    await db.delete(db_anuncio)
    await db.commit()
    return {"message": "Anuncio eliminado"}