from pydantic import BaseModel

class QuestionBase(BaseModel):
    contenido: str

class QuestionCreate(QuestionBase):
    usuario_id: int  # Agregamos usuario_id aquí para recibirlo en la creación de preguntas

class QuestionResponse(QuestionBase):
    id: int
    usuario_id: int
