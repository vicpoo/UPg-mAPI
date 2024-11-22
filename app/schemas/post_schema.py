from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class PostBase(BaseModel):
    descripcion: str

class PostCreate(PostBase):
    usuario_id: int

class PostResponse(PostBase):
    id: int
    usuario_id: Optional[int]
    imagen: Optional[str] = None  # Base64 para imágenes
    fecha_creacion: datetime  # Agregamos el campo fecha

    class Config:
        orm_mode = True
