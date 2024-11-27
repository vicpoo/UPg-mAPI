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
def encode_image(image_data: bytes | str) -> str:
    """Convierte los datos de la imagen en formato base64."""
    if isinstance(image_data, str):
        return f"data:image/jpeg;base64,{image_data}"
    elif isinstance(image_data, bytes):
        return f"data:image/jpeg;base64,{base64.b64encode(image_data).decode('utf-8')}"
    return None

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
        usuario_id=respuesta.usuario_id,  # Asocia la respuesta al usuario proporcionado
    )
    db.add(nueva_respuesta)
    await db.commit()
    await db.refresh(nueva_respuesta)

    # Adjuntar datos del usuario para la respuesta
    usuario_data = {
        "id": usuario.id,
        "nombre_usuario": usuario.nombre_usuario,
        "correo": usuario.correo,
        "descripcion": usuario.descripcion,
        "foto_perfil": encode_image(usuario.foto_perfil) if usuario.foto_perfil else None
    }

    # Devuelve la respuesta creada con información del usuario
    return {
        "id": nueva_respuesta.id,
        "contenido": nueva_respuesta.contenido,
        "pregunta_id": nueva_respuesta.pregunta_id,
        "fecha_creacion": nueva_respuesta.fecha_creacion,
        "usuario": usuario_data,  # Objeto usuario
    }



from sqlalchemy.orm import selectinload

@respuestaRoutes.get("/preguntas/{question_id}/respuestas/", response_model=list[RespuestaOut])
async def obtener_respuestas(question_id: int, db: AsyncSession = Depends(get_db)):
    # Obtén las respuestas relacionadas con la pregunta y carga los usuarios asociados
    query = await db.execute(
        select(Respuesta)
        .options(selectinload(Respuesta.usuario))  # Cargar la relación usuario
        .where(Respuesta.pregunta_id == question_id)
    )
    respuestas = query.scalars().all()

    # Construye la respuesta enriquecida
    resultado = []
    for respuesta in respuestas:
        usuario = respuesta.usuario
        if usuario and usuario.foto_perfil:
            usuario.foto_perfil = encode_image(usuario.foto_perfil)  # Convertir la foto de perfil a base64
        
        # Construimos la respuesta incluyendo el objeto `usuario`
        resultado.append({
            "id": respuesta.id,
            "contenido": respuesta.contenido,
            "pregunta_id": respuesta.pregunta_id,
            "fecha_creacion": respuesta.fecha_creacion,
            "usuario": {
                "id": usuario.id,
                "nombre_usuario": usuario.nombre_usuario,
                "correo": usuario.correo,
                "descripcion": usuario.descripcion,
                "foto_perfil": usuario.foto_perfil if usuario else None  # Foto convertida a base64
            }
        })

    return resultado
