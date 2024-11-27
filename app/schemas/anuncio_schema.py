# schemas/anuncio_schema.py

from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AnuncioBase(BaseModel):
    imagen: Optional[str] = None  # Base64 de la imagen

class AnuncioResponse(AnuncioBase):
    id: int
    imagen: Optional[str] = None  # La imagen codificada en base64

    class Config:
        orm_mode = True