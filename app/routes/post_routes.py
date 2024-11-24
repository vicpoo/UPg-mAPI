from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from sqlalchemy import desc
from app.models.post import Post
from app.models.User import User
from app.schemas.post_schema import PostResponse
from app.shared.config.db import get_db
import base64
import io
from PIL import Image
from datetime import datetime

postRoutes = APIRouter()

def resize_image(image_data, max_size=(800, 800)):
    """Redimensiona la imagen para no exceder el tamaño permitido."""
    image = Image.open(io.BytesIO(image_data))
    if image.mode == 'RGBA':
        image = image.convert('RGB')
    image.thumbnail(max_size, Image.LANCZOS)
    output = io.BytesIO()
    image.save(output, format="JPEG")
    return output.getvalue()


@postRoutes.post('/post/', response_model=PostResponse, status_code=status.HTTP_201_CREATED)
async def create_post(
    descripcion: str = Form(...),
    usuario_id: int = Form(...),
    imagen: UploadFile = File(...),
    db: AsyncSession = Depends(get_db)
):
    """Crea una nueva publicación con una imagen obligatoria."""
    # Verificar que el usuario existe
    result = await db.execute(select(User).where(User.id == usuario_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Leer y redimensionar la imagen
    image_data = await imagen.read()
    imagen_data = resize_image(image_data)

    # Crear la nueva publicación
    new_post = Post(
        descripcion=descripcion,
        usuario_id=usuario_id,
        imagen=imagen_data,
        fecha_creacion=datetime.utcnow()
    )
    db.add(new_post)
    await db.commit()

    # Cargar el usuario relacionado para evitar problemas en la serialización
    await db.refresh(new_post)

    # Procesar la imagen para enviarla como base64 en la respuesta
    if new_post.imagen:
        new_post.imagen = base64.b64encode(new_post.imagen).decode('utf-8')

    if new_post.usuario and new_post.usuario.foto_perfil:
        if isinstance(new_post.usuario.foto_perfil, bytes):
            new_post.usuario.foto_perfil = f"data:image/jpeg;base64,{base64.b64encode(new_post.usuario.foto_perfil).decode('utf-8')}"
        else:
            new_post.usuario.foto_perfil = None

    return new_post


@postRoutes.get('/posts/', response_model=List[PostResponse])
async def get_posts(db: AsyncSession = Depends(get_db)):
    """Recuperar todas las publicaciones, con datos del usuario y ordenadas por fecha."""
    result = await db.execute(
        select(Post)
        .options(joinedload(Post.usuario))  # Carga los datos del usuario relacionado
        .order_by(desc(Post.fecha_creacion))
    )
    posts = result.scalars().all()

    # Procesar imágenes en Base64
    for post in posts:
        if post.imagen:
            post.imagen = f"data:image/jpeg;base64,{base64.b64encode(post.imagen).decode('utf-8')}"
        if post.usuario and post.usuario.foto_perfil:
             if isinstance(post.usuario.foto_perfil, bytes):  # Confirma que es binario
                post.usuario.foto_perfil = f"data:image/jpeg;base64,{base64.b64encode(post.usuario.foto_perfil).decode('utf-8')}"
        else:
         post.usuario.foto_perfil = None


    return posts


@postRoutes.get('/posts/user/{usuario_id}', response_model=List[PostResponse])
async def get_user_posts(usuario_id: int, db: AsyncSession = Depends(get_db)):
    """Obtiene las publicaciones realizadas por un usuario específico, incluyendo sus datos."""
    result = await db.execute(
        select(Post)
        .options(joinedload(Post.usuario))  # Carga el usuario relacionado
        .where(Post.usuario_id == usuario_id)
        .order_by(desc(Post.fecha_creacion))
    )
    posts = result.scalars().all()

    for post in posts:
        if post.imagen:
            post.imagen = f"data:image/jpeg;base64,{base64.b64encode(post.imagen).decode('utf-8')}"
        if post.usuario and post.usuario.foto_perfil:
            if isinstance(post.usuario.foto_perfil, bytes):
                post.usuario.foto_perfil = f"data:image/jpeg;base64,{base64.b64encode(post.usuario.foto_perfil).decode('utf-8')}"
            else:
                post.usuario.foto_perfil = None

    return posts

@postRoutes.get('/post/{post_id}', response_model=PostResponse)
async def get_post_by_id(post_id: int, db: AsyncSession = Depends(get_db)):
    """Obtiene una publicación por ID, incluyendo los datos del usuario."""
    result = await db.execute(
        select(Post).options(joinedload(Post.usuario)).where(Post.id == post_id)
    )
    post = result.scalar_one_or_none()
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")

    if post.imagen:
        post.imagen = f"data:image/jpeg;base64,{base64.b64encode(post.imagen).decode('utf-8')}"
    if post.usuario and post.usuario.foto_perfil:
        if isinstance(post.usuario.foto_perfil, bytes):
            post.usuario.foto_perfil = f"data:image/jpeg;base64,{base64.b64encode(post.usuario.foto_perfil).decode('utf-8')}"
        else:
            post.usuario.foto_perfil = None

    return post

@postRoutes.put('/post/{post_id}', response_model=PostResponse)
async def update_post(
    post_id: int,
    descripcion: str = Form(...),
    usuario_id: int = Form(...),
    imagen: UploadFile = File(None),
    db: AsyncSession = Depends(get_db)
):
    """Update an existing post by ID with optional image upload."""
    result = await db.execute(select(Post).where(Post.id == post_id))
    db_post = result.scalar_one_or_none()
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")

    db_post.descripcion = descripcion
    db_post.usuario_id = usuario_id

    if imagen:
        db_post.imagen = await imagen.read()

    await db.commit()
    await db.refresh(db_post)

    if db_post.imagen:
        db_post.imagen = base64.b64encode(db_post.imagen).decode('utf-8')

    return db_post

@postRoutes.delete('/post/{post_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: int, db: AsyncSession = Depends(get_db)):
    """Delete a post by ID."""
    result = await db.execute(select(Post).where(Post.id == post_id))
    db_post = result.scalar_one_or_none()
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    await db.delete(db_post)
    await db.commit()
    return {"message": "Post deleted"}
