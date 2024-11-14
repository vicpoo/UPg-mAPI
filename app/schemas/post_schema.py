from pydantic import BaseModel
from typing import Optional

class PostBase(BaseModel):
    descripcion: str
    imagen: Optional[bytes] = None

class PostCreate(PostBase):
    usuario_id: int

class PostResponse(PostBase):
    id: int
    usuario_id: Optional[int]  # Hacer usuario_id opcional aquí
