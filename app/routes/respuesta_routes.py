from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.User import User
from app.models.question import Question
from app.models.respuesta import Respuesta
from app.schemas.respuesta_schema import RespuestaOut, RespuestaCreate
from app.shared.config.db import get_db
import base64

respuestaRoutes = APIRouter()

# Helper para convertir imágenes a Base64
def encode_image(image: bytes) -> str:
    return base64.b64encode(image).decode('utf-8') if image else ""  # Devuelve una cadena vacía si no hay imagen



@respuestaRoutes.post("/respuestas/", response_model=RespuestaOut, status_code=status.HTTP_201_CREATED)
async def crear_respuesta(respuesta: RespuestaCreate, db: AsyncSession = Depends(get_db)):
    # Verifica si la pregunta existe
    pregunta_query = await db.execute(select(Question).where(Question.id == respuesta.pregunta_id))
    pregunta = pregunta_query.scalar_one_or_none()
    if not pregunta:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pregunta no encontrada")

    # Verifica si el usuario existe
    usuario_query = await db.execute(select(User).where(User.id == respuesta.usuario_id))
    usuario = usuario_query.scalar_one_or_none()
    if not usuario:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")

    # Crea una nueva respuesta
    nueva_respuesta = Respuesta(
        contenido=respuesta.contenido,
        pregunta_id=respuesta.pregunta_id,
        usuario_id=respuesta.usuario_id,
    )
    db.add(nueva_respuesta)
    await db.commit()
    await db.refresh(nueva_respuesta)

    # Devuelve la respuesta creada, con información adicional del usuario
    return {
        "id": nueva_respuesta.id,
        "contenido": nueva_respuesta.contenido,
        "pregunta_id": nueva_respuesta.pregunta_id,
        "fecha_creacion": nueva_respuesta.fecha_creacion,
        "usuario_nombre": usuario.nombre_usuario,
        "usuario_foto": encode_image(usuario.foto_perfil),  # Maneja imágenes vacías correctamente
    }


@respuestaRoutes.get("/preguntas/{question_id}/respuestas/", response_model=list[RespuestaOut], status_code=status.HTTP_200_OK)
async def obtener_respuestas(pregunta_id: int, db: AsyncSession = Depends(get_db)):
    # Obtén las respuestas relacionadas con la pregunta
    query = await db.execute(
        select(Respuesta).where(Respuesta.pregunta_id == pregunta_id)
    )
    respuestas = query.scalars().all()

    # Consulta usuarios relacionados en una sola operación
    usuario_ids = {respuesta.usuario_id for respuesta in respuestas}
    usuarios_query = await db.execute(select(User).where(User.id.in_(usuario_ids)))
    usuarios = {user.id: user for user in usuarios_query.scalars().all()}

    # Construye la respuesta enriquecida
    resultado = []
    for respuesta in respuestas:
        usuario = usuarios.get(respuesta.usuario_id)
        resultado.append({
            "id": respuesta.id,
            "contenido": respuesta.contenido,
            "pregunta_id": respuesta.pregunta_id,
            "fecha_creacion": respuesta.fecha_creacion,
            "usuario_nombre": usuario.nombre_usuario if usuario else None,
            "usuario_foto": encode_image(usuario.foto_perfil) if usuario and usuario.foto_perfil else None,
        })

    return resultado
