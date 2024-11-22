from pydantic import BaseModel
from datetime import datetime

class QuestionBase(BaseModel):
    contenido: str

class QuestionCreate(QuestionBase):
    usuario_id: int  # Agregamos usuario_id aquí para recibirlo en la creación de preguntas

class QuestionResponse(QuestionBase):
    id: int
    usuario_id: int
    fecha_creacion: datetime  # Incluir fecha en la respuesta

    class Config:
        orm_mode = True  # Permite a Pydantic mapear datos desde SQLAlchemy
