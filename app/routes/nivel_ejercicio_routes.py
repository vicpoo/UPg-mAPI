from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.nivel_ejercicio import NivelEjercicio
from app.schemas.nivel_ejercicio_schema import NivelEjercicioCreate, NivelEjercicioResponse, NivelEjercicioUpdate
from app.shared.config.db import get_db
from typing import List

nivelRoutes = APIRouter()

# Crear un nivel
@nivelRoutes.post('/niveles/', response_model=NivelEjercicioResponse, status_code=status.HTTP_201_CREATED)
async def create_nivel(nivel: NivelEjercicioCreate, db: AsyncSession = Depends(get_db)):
    nuevo_nivel = NivelEjercicio(nivel=nivel.nivel)
    db.add(nuevo_nivel)
    await db.commit()
    await db.refresh(nuevo_nivel)
    return nuevo_nivel

# Obtener todos los niveles
@nivelRoutes.get('/niveles/', response_model=List[NivelEjercicioResponse])
async def get_all_niveles(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(NivelEjercicio))
    return result.scalars().all()
