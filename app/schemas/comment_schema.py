from pydantic import BaseModel

class CommentBase(BaseModel):
    contenido: str

class CommentCreate(CommentBase):
    pass

class CommentResponse(CommentBase):
    id: int
    publicacion_id: int
    usuario_id: int
