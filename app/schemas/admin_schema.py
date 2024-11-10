from pydantic import BaseModel

class AdminBase(BaseModel):
    nombre: str
    apellido: str

class AdminCreate(AdminBase):
    pass

class AdminResponse(AdminBase):
    id: int
    usuario_id: int
