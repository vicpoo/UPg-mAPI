from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.PorcentajeGrasa import PorcentajeGrasa
from app.schemas.PorcentajeGrasa_schema import PorcentajeGrasaCreate, PorcentajeGrasaResponse
from app.shared.config.db import get_db
from app.models.user import User  # Importa correctamente el modelo User
from app.routes.user_routes import get_current_user  # Para obtener al usuario logueado

porcentajeGrasaRoutes = APIRouter()

@porcentajeGrasaRoutes.post("/Grasa", response_model=PorcentajeGrasaResponse, status_code=201)
async def create_porcentaje_grasa(
    data: PorcentajeGrasaCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Aquí ya no es necesario calcular el resultado, se toma el valor de `data.resultado`
    nuevo_registro = PorcentajeGrasa(
        user_id=current_user.id,
        genero=data.genero,
        altura=data.altura,
        cintura=data.cintura,
        resultado=data.resultado  # Usar el resultado recibido
    )
    db.add(nuevo_registro)
    await db.commit()
    await db.refresh(nuevo_registro)

    return PorcentajeGrasaResponse.from_create(data, current_user.id)

@porcentajeGrasaRoutes.get("/Grasa/historial", response_model=list[PorcentajeGrasaResponse])
async def get_historial_porcentaje_grasa(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)  # Asegura que el usuario logueado está consultando
):
    result = await db.execute(select(PorcentajeGrasa).where(PorcentajeGrasa.user_id == current_user.id))
    registros = result.scalars().all()
    return registros
