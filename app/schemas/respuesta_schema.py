from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class RespuestaCreate(BaseModel):
    contenido: str
    pregunta_id: int
    usuario_id: int

class RespuestaOut(BaseModel):
    id: int
    contenido: str
    pregunta_id: int
    fecha_creacion: datetime
    usuario_nombre: str
    usuario_foto: Optional[str]


    class Config:
        orm_mode = True
