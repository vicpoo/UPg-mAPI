from pydantic import BaseModel

class PostBase(BaseModel):
    descripcion: str
    imagen: bytes | None = None

class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    id: int
    usuario_id: int
