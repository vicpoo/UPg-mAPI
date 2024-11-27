from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.ubicaciones import Ubicaciones
from app.schemas.ubicaciones_schema import UbicacionCreate, UbicacionResponse, UbicacionUpdate
from app.shared.config.db import get_db
from typing import List

ubicacionesRoutes = APIRouter()

# Crear una ubicación
@ubicacionesRoutes.post('/ubicaciones/', response_model=UbicacionResponse, status_code=status.HTTP_201_CREATED)
async def create_ubicacion(ubicacion: UbicacionCreate, db: AsyncSession = Depends(get_db)):
    nueva_ubicacion = Ubicaciones(ubicacion=ubicacion.ubicacion)
    db.add(nueva_ubicacion)
    await db.commit()
    await db.refresh(nueva_ubicacion)
    return nueva_ubicacion
