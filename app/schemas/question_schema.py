from pydantic import BaseModel

class QuestionBase(BaseModel):
    contenido: str

class QuestionCreate(QuestionBase):
    pass

class QuestionResponse(QuestionBase):
    id: int
    usuario_id: int
