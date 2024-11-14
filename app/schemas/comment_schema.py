from pydantic import BaseModel

class CommentBase(BaseModel):
    contenido: str

class CommentCreate(CommentBase):
    publicacion_id: int
    usuario_id: int

class CommentResponse(CommentBase):
    id: int
    publicacion_id: int
    usuario_id: int
