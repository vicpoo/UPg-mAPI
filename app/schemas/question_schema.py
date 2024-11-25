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

class QuestionBase(BaseModel):
    contenido: str

class QuestionCreate(QuestionBase):
    usuario_id: int  # Agregar ID del usuario para creación

class QuestionResponse(QuestionBase):
    id: int
    usuario_id: int
    fecha_creacion: datetime
    usuario: Optional[UserResponse]  # Relación con el usuario

    class Config:
        orm_mode = True
