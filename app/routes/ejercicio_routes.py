from typing import List, Optional
from fastapi import APIRouter, HTTPException, status, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from app.models.ejercicio import Ejercicio
from app.schemas.ejercicio_schema import EjercicioResponse, EjercicioCreate, EjercicioUpdate
from app.shared.config.db import async_session
import base64
import io
from PIL import Image

ejercicioRoutes = APIRouter()

# Utility function to resize and process images
def resize_image(image_data, max_size=(800, 800)):
    """Redimensiona la imagen para no exceder el tamaño permitido."""
    image = Image.open(io.BytesIO(image_data))
    if image.mode == 'RGBA':
        image = image.convert('RGB')
    image.thumbnail(max_size, Image.LANCZOS)
    output = io.BytesIO()
    image.save(output, format="JPEG")
    return output.getvalue()

@ejercicioRoutes.post('/ejercicios/', response_model=EjercicioResponse, status_code=status.HTTP_201_CREATED)
async def create_ejercicio(
    titulo: str = Form(...),
    resumen: str = Form(...),
    tiempo_descanso: int = Form(...),
    repeticiones: int = Form(...),
    imagen: UploadFile = File(...),
):
    """Crea un nuevo ejercicio con validaciones para nivel y ubicación específicas."""
    nivel_id = 1  # Nivel básico
    ubicacion_id = 1  # Ubicación casa

    # Procesar la imagen
    image_data = await imagen.read()
    resized_image = resize_image(image_data)

    async with async_session() as db:
        async with db.begin():
            # Crear el nuevo ejercicio
            new_ejercicio = Ejercicio(
                titulo=titulo,
                resumen=resumen,
                nivel_id=nivel_id,
                tiempo_descanso=tiempo_descanso,
                repeticiones=repeticiones,
                imagen=resized_image,
                ubicacion_id=ubicacion_id,
            )
            db.add(new_ejercicio)
        await db.commit()
        await db.refresh(new_ejercicio)

    # Convertir la imagen a base64 para la respuesta
    if new_ejercicio.imagen:
        new_ejercicio.imagen = f"data:image/jpeg;base64,{base64.b64encode(new_ejercicio.imagen).decode('utf-8')}"

    return new_ejercicio





# Filtro para level_id: 1, ubicacion_id: 1
@ejercicioRoutes.get('/ejercicios/', response_model=List[EjercicioResponse])
async def get_ejercicios_level1():
    nivel_id = 1
    ubicacion_id = 1

    async with async_session() as db:
        result = await db.execute(
            select(Ejercicio)
            .where(Ejercicio.nivel_id == nivel_id)
            .where(Ejercicio.ubicacion_id == ubicacion_id)
        )
        ejercicios = result.scalars().all()

    for ejercicio in ejercicios:
        if ejercicio.imagen:
            ejercicio.imagen = f"data:image/jpeg;base64,{base64.b64encode(ejercicio.imagen).decode('utf-8')}"

    return ejercicios


@ejercicioRoutes.put('/ejercicios/{ejercicio_id}', response_model=EjercicioResponse)
async def update_ejercicio(
    ejercicio_id: int,
    titulo: str = Form(...),
    resumen: str = Form(...),
    tiempo_descanso: int = Form(...),
    repeticiones: int = Form(...),
    imagen: Optional[UploadFile] = File(None),
):
    """Actualiza un ejercicio existente. Solo permite actualizar los campos del POST."""
    async with async_session() as db:
        result = await db.execute(select(Ejercicio).where(Ejercicio.id == ejercicio_id))
        ejercicio = result.scalar_one_or_none()

        if not ejercicio:
            raise HTTPException(status_code=404, detail="Ejercicio no encontrado")

        # Actualizar los datos
        ejercicio.titulo = titulo
        ejercicio.resumen = resumen
        ejercicio.tiempo_descanso = tiempo_descanso
        ejercicio.repeticiones = repeticiones

        # Procesar nueva imagen si se envía
        if imagen:
            image_data = await imagen.read()
            ejercicio.imagen = resize_image(image_data)

        await db.commit()
        await db.refresh(ejercicio)

    # Convertir imagen a base64 para la respuesta
    if ejercicio.imagen:
        ejercicio.imagen = f"data:image/jpeg;base64,{base64.b64encode(ejercicio.imagen).decode('utf-8')}"

    return ejercicio

@ejercicioRoutes.delete('/ejercicios/{ejercicio_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_ejercicio(ejercicio_id: int):
    """Elimina un ejercicio por ID."""
    async with async_session() as db:
        result = await db.execute(select(Ejercicio).where(Ejercicio.id == ejercicio_id))
        ejercicio = result.scalar_one_or_none()

        if not ejercicio:
            raise HTTPException(status_code=404, detail=f"Ejercicio con ID {ejercicio_id} no encontrado")

        await db.delete(ejercicio)
        await db.commit()

    return {"message": "Ejercicio eliminado"}


# -------------------------------
# CRUD PARA level_id: 2, ubicacion_id: 2
# -------------------------------

@ejercicioRoutes.post('/ejercicios-level2/', response_model=EjercicioResponse, status_code=status.HTTP_201_CREATED)
async def create_ejercicio_level2(
    titulo: str = Form(...),
    resumen: str = Form(...),
    tiempo_descanso: int = Form(...),
    repeticiones: int = Form(...),
    imagen: UploadFile = File(...),
):
    nivel_id = 2
    ubicacion_id = 2

    image_data = await imagen.read()
    resized_image = resize_image(image_data)

    async with async_session() as db:
        async with db.begin():
            new_ejercicio = Ejercicio(
                titulo=titulo,
                resumen=resumen,
                nivel_id=nivel_id,
                tiempo_descanso=tiempo_descanso,
                repeticiones=repeticiones,
                imagen=resized_image,
                ubicacion_id=ubicacion_id,
            )
            db.add(new_ejercicio)
        await db.commit()
        await db.refresh(new_ejercicio)

    if new_ejercicio.imagen:
        new_ejercicio.imagen = f"data:image/jpeg;base64,{base64.b64encode(new_ejercicio.imagen).decode('utf-8')}"

    return new_ejercicio


@ejercicioRoutes.put('/ejercicios-level2/{ejercicio_id}', response_model=EjercicioResponse)
async def update_ejercicio_level2(
    ejercicio_id: int,
    titulo: str = Form(...),
    resumen: str = Form(...),
    tiempo_descanso: int = Form(...),
    repeticiones: int = Form(...),
    imagen: Optional[UploadFile] = File(None),
):
    nivel_id = 2
    ubicacion_id = 2

    async with async_session() as db:
        result = await db.execute(select(Ejercicio).where(Ejercicio.id == ejercicio_id, Ejercicio.nivel_id == nivel_id, Ejercicio.ubicacion_id == ubicacion_id))
        ejercicio = result.scalar_one_or_none()

        if not ejercicio:
            raise HTTPException(status_code=404, detail="Ejercicio no encontrado")

        ejercicio.titulo = titulo
        ejercicio.resumen = resumen
        ejercicio.tiempo_descanso = tiempo_descanso
        ejercicio.repeticiones = repeticiones

        if imagen:
            image_data = await imagen.read()
            ejercicio.imagen = resize_image(image_data)

        await db.commit()
        await db.refresh(ejercicio)

    if ejercicio.imagen:
        ejercicio.imagen = f"data:image/jpeg;base64,{base64.b64encode(ejercicio.imagen).decode('utf-8')}"

    return ejercicio


# -------------------------------
# GET POR FILTRO
# -------------------------------



# Filtro para level_id: 2, ubicacion_id: 2
@ejercicioRoutes.get('/ejercicios-level2/', response_model=List[EjercicioResponse])
async def get_ejercicios_level2():
    nivel_id = 2
    ubicacion_id = 2

    async with async_session() as db:
        result = await db.execute(
            select(Ejercicio)
            .where(Ejercicio.nivel_id == nivel_id)
            .where(Ejercicio.ubicacion_id == ubicacion_id)
        )
        ejercicios = result.scalars().all()

    for ejercicio in ejercicios:
        if ejercicio.imagen:
            ejercicio.imagen = f"data:image/jpeg;base64,{base64.b64encode(ejercicio.imagen).decode('utf-8')}"

    return ejercicios

# -------------------------------
# CRUD PARA level_id: 3, ubicacion_id: 1
# -------------------------------

@ejercicioRoutes.post('/ejercicios-level3-ubicacion1/', response_model=EjercicioResponse, status_code=status.HTTP_201_CREATED)
async def create_ejercicio_level3_ubicacion1(
    titulo: str = Form(...),
    resumen: str = Form(...),
    tiempo_descanso: int = Form(...),
    repeticiones: int = Form(...),
    imagen: UploadFile = File(...),
):
    nivel_id = 3
    ubicacion_id = 1

    image_data = await imagen.read()
    resized_image = resize_image(image_data)

    async with async_session() as db:
        async with db.begin():
            new_ejercicio = Ejercicio(
                titulo=titulo,
                resumen=resumen,
                nivel_id=nivel_id,
                tiempo_descanso=tiempo_descanso,
                repeticiones=repeticiones,
                imagen=resized_image,
                ubicacion_id=ubicacion_id,
            )
            db.add(new_ejercicio)
        await db.commit()
        await db.refresh(new_ejercicio)

    if new_ejercicio.imagen:
        new_ejercicio.imagen = f"data:image/jpeg;base64,{base64.b64encode(new_ejercicio.imagen).decode('utf-8')}"

    return new_ejercicio


@ejercicioRoutes.put('/ejercicios-level3-ubicacion1/{ejercicio_id}', response_model=EjercicioResponse)
async def update_ejercicio_level3_ubicacion1(
    ejercicio_id: int,
    titulo: str = Form(...),
    resumen: str = Form(...),
    tiempo_descanso: int = Form(...),
    repeticiones: int = Form(...),
    imagen: Optional[UploadFile] = File(None),
):
    nivel_id = 3
    ubicacion_id = 1

    async with async_session() as db:
        result = await db.execute(select(Ejercicio).where(Ejercicio.id == ejercicio_id, Ejercicio.nivel_id == nivel_id, Ejercicio.ubicacion_id == ubicacion_id))
        ejercicio = result.scalar_one_or_none()

        if not ejercicio:
            raise HTTPException(status_code=404, detail="Ejercicio no encontrado")

        ejercicio.titulo = titulo
        ejercicio.resumen = resumen
        ejercicio.tiempo_descanso = tiempo_descanso
        ejercicio.repeticiones = repeticiones

        if imagen:
            image_data = await imagen.read()
            ejercicio.imagen = resize_image(image_data)

        await db.commit()
        await db.refresh(ejercicio)

    if ejercicio.imagen:
        ejercicio.imagen = f"data:image/jpeg;base64,{base64.b64encode(ejercicio.imagen).decode('utf-8')}"

    return ejercicio


@ejercicioRoutes.get('/ejercicios-level3-ubicacion1/', response_model=List[EjercicioResponse])
async def get_ejercicios_level3_ubicacion1():
    nivel_id = 3
    ubicacion_id = 1

    async with async_session() as db:
        result = await db.execute(select(Ejercicio).where(Ejercicio.nivel_id == nivel_id, Ejercicio.ubicacion_id == ubicacion_id))
        ejercicios = result.scalars().all()

    for ejercicio in ejercicios:
        if ejercicio.imagen:
            ejercicio.imagen = f"data:image/jpeg;base64,{base64.b64encode(ejercicio.imagen).decode('utf-8')}"

    return ejercicios



# -------------------------------
# CRUD PARA level_id: 3, ubicacion_id: 2
# -------------------------------

@ejercicioRoutes.post('/ejercicios-level3-ubicacion2/', response_model=EjercicioResponse, status_code=status.HTTP_201_CREATED)
async def create_ejercicio_level3_ubicacion2(
    titulo: str = Form(...),
    resumen: str = Form(...),
    tiempo_descanso: int = Form(...),
    repeticiones: int = Form(...),
    imagen: UploadFile = File(...),
):
    nivel_id = 3
    ubicacion_id = 2

    image_data = await imagen.read()
    resized_image = resize_image(image_data)

    async with async_session() as db:
        async with db.begin():
            new_ejercicio = Ejercicio(
                titulo=titulo,
                resumen=resumen,
                nivel_id=nivel_id,
                tiempo_descanso=tiempo_descanso,
                repeticiones=repeticiones,
                imagen=resized_image,
                ubicacion_id=ubicacion_id,
            )
            db.add(new_ejercicio)
        await db.commit()
        await db.refresh(new_ejercicio)

    if new_ejercicio.imagen:
        new_ejercicio.imagen = f"data:image/jpeg;base64,{base64.b64encode(new_ejercicio.imagen).decode('utf-8')}"

    return new_ejercicio


@ejercicioRoutes.put('/ejercicios-level3-ubicacion2/{ejercicio_id}', response_model=EjercicioResponse)
async def update_ejercicio_level3_ubicacion2(
    ejercicio_id: int,
    titulo: str = Form(...),
    resumen: str = Form(...),
    tiempo_descanso: int = Form(...),
    repeticiones: int = Form(...),
    imagen: Optional[UploadFile] = File(None),
):
    nivel_id = 3
    ubicacion_id = 2

    async with async_session() as db:
        result = await db.execute(select(Ejercicio).where(Ejercicio.id == ejercicio_id, Ejercicio.nivel_id == nivel_id, Ejercicio.ubicacion_id == ubicacion_id))
        ejercicio = result.scalar_one_or_none()

        if not ejercicio:
            raise HTTPException(status_code=404, detail="Ejercicio no encontrado")

        ejercicio.titulo = titulo
        ejercicio.resumen = resumen
        ejercicio.tiempo_descanso = tiempo_descanso
        ejercicio.repeticiones = repeticiones

        if imagen:
            image_data = await imagen.read()
            ejercicio.imagen = resize_image(image_data)

        await db.commit()
        await db.refresh(ejercicio)

    if ejercicio.imagen:
        ejercicio.imagen = f"data:image/jpeg;base64,{base64.b64encode(ejercicio.imagen).decode('utf-8')}"

    return ejercicio


@ejercicioRoutes.get('/ejercicios-level3-ubicacion2/', response_model=List[EjercicioResponse])
async def get_ejercicios_level3_ubicacion2():
    nivel_id = 3
    ubicacion_id = 2

    async with async_session() as db:
        result = await db.execute(select(Ejercicio).where(Ejercicio.nivel_id == nivel_id, Ejercicio.ubicacion_id == ubicacion_id))
        ejercicios = result.scalars().all()

    for ejercicio in ejercicios:
        if ejercicio.imagen:
            ejercicio.imagen = f"data:image/jpeg;base64,{base64.b64encode(ejercicio.imagen).decode('utf-8')}"

    return ejercicios
