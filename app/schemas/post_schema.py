from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class UserResponse(BaseModel):
    id: int
    nombre_usuario: str
    correo: str
    descripcion: Optional[str] = None
    foto_perfil: Optional[str] = None  # Base64 de la foto

    class Config:
        orm_mode = True


class PostBase(BaseModel):
    descripcion: str


class PostResponse(PostBase):
    id: int
    usuario_id: int
    imagen: Optional[str] = None  # Base64 para imágenes
    fecha_creacion: datetime
    usuario: Optional[UserResponse]  # Relación con el usuario

    class Config:
        orm_mode = True
