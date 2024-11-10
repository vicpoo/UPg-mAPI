from pydantic import BaseModel

class LikeBase(BaseModel):
    publicacion_id: int
    usuario_id: int

class LikeCreate(LikeBase):
    pass

class LikeResponse(LikeBase):
    id: int
