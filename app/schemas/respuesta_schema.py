from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class RespuestaCreate(BaseModel):
    contenido: str
    pregunta_id: int
    usuario_id: int


class UsuarioOut(BaseModel):
    id: int
    nombre_usuario: str
    correo: str
    descripcion: Optional[str]
    foto_perfil: Optional[str]

    class Config:
        orm_mode = True

class RespuestaOut(BaseModel):
    id: int
    contenido: str
    pregunta_id: int
    fecha_creacion: datetime
    usuario: UsuarioOut  # Aquí agregamos el objeto usuario

    class Config:
        orm_mode = True

