from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.post import Post
from app.models.user import User
from app.schemas.post_schema import PostResponse
from app.shared.config.db import get_db
import base64
import io
from PIL import Image



postRoutes = APIRouter()

def resize_image(image_data, max_size=(800, 800)):
    """Redimensiona la imagen para no exceder el tamaño permitido."""
    image = Image.open(io.BytesIO(image_data))
    image.thumbnail(max_size, Image.LANCZOS)  # Reemplazamos ANTIALIAS por LANCZOS
    output = io.BytesIO()
    image.save(output, format="JPEG")  # Guardamos en JPEG para compresión eficiente
    return output.getvalue()

@postRoutes.post('/post/', response_model=PostResponse, status_code=status.HTTP_201_CREATED)
async def create_post(
    descripcion: str = Form(...),
    usuario_id: int = Form(...),
    imagen: UploadFile = File(...),  # Ahora es obligatorio subir una imagen
    db: AsyncSession = Depends(get_db)
):
    """Crea una nueva publicación con una imagen obligatoria."""
    # Verificar que el usuario existe
    result = await db.execute(select(User).where(User.id == usuario_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    image_data = await imagen.read()
    imagen_data = resize_image(image_data)  # Redimensionar imagen

    new_post = Post(
        descripcion=descripcion,
        usuario_id=usuario_id,
        imagen=imagen_data
    )
    db.add(new_post)
    await db.commit()
    await db.refresh(new_post)

    if new_post.imagen:
        new_post.imagen = base64.b64encode(new_post.imagen).decode('utf-8')

    return new_post


@postRoutes.get('/posts/', response_model=List[PostResponse])
async def get_posts(db: AsyncSession = Depends(get_db)):
    """Recuperar todas las publicaciones."""
    result = await db.execute(select(Post))
    posts = result.scalars().all()

    for post in posts:
        if post.imagen:
            post.imagen = f"data:image/jpeg;base64,{base64.b64encode(post.imagen).decode('utf-8')}"

    return posts

@postRoutes.get('/posts/user/{usuario_id}', response_model=List[PostResponse])
async def get_user_posts(usuario_id: int, db: AsyncSession = Depends(get_db)):
    """Obtiene las publicaciones realizadas por un usuario específico."""
    result = await db.execute(select(Post).where(Post.usuario_id == usuario_id))
    posts = result.scalars().all()

    for post in posts:
        if post.imagen:
            post.imagen = f"data:image/jpeg;base64,{base64.b64encode(post.imagen).decode('utf-8')}"

    return posts


@postRoutes.get('/post/{post_id}', response_model=PostResponse)
async def get_post_by_id(post_id: int, db: AsyncSession = Depends(get_db)):
    """Retrieve a post by ID with the image as a Base64 string."""
    result = await db.execute(select(Post).where(Post.id == post_id))
    post = result.scalar_one_or_none()
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")

    if post.imagen:
        post.imagen = base64.b64encode(post.imagen).decode('utf-8')

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
