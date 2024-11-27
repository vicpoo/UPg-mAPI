from pydantic import BaseModel
from typing import Optional

class EjercicioBase(BaseModel):
    titulo: str
    resumen: str
    nivel_id: int
    tiempo_descanso: int
    repeticiones: int
    ubicacion_id: int

class EjercicioCreate(EjercicioBase):
    # Accepting image as base64 string instead of bytes for easier handling in the frontend
    imagen: Optional[str] = None  # Image should be base64 encoded when creating the exercise

class EjercicioUpdate(BaseModel):
    titulo: Optional[str] = None
    resumen: Optional[str] = None
    nivel_id: Optional[int] = None
    tiempo_descanso: Optional[int] = None
    repeticiones: Optional[int] = None
    ubicacion_id: Optional[int] = None
    imagen: Optional[str] = None  # Image field should be a base64 string for updates as well

class EjercicioResponse(EjercicioBase):
    id: int
    imagen: Optional[str] = None  # Base64 image string in the response

    class Config:
        orm_mode = True
