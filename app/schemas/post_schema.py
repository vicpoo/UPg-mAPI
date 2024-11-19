from pydantic import BaseModel
from typing import Optional

class PostBase(BaseModel):
    descripcion: str

class PostCreate(PostBase):
    usuario_id: int

class PostResponse(PostBase):
    id: int
    usuario_id: Optional[int]
    imagen: Optional[str] = None  # Base64 para imágenes en las respuestas

    class Config:
        orm_mode = True
